from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.config import settings
from backend.logger import setup_logger

logger = setup_logger(__name__)

# Create the async engine — this is the connection to Supabase PostgreSQL
# pool_pre_ping=True means SQLAlchemy checks the connection is alive before using it
engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=False,  # Set to True to log all SQL queries (useful for debugging)
)

# Session factory — creates new DB sessions for each request
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency — yields a DB session for each request.
    Automatically closes the session when the request is done.

    Usage in routes:
        async def my_route(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables() -> None:
    """
    Create all tables defined in models.py if they don't exist yet.
    Called once at app startup.
    """
    from backend.db.models import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
