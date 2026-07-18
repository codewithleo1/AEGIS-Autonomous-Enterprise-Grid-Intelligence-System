from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select

from backend.config import settings
from backend.db.models import Agent, Employee
from backend.db.postgres import AsyncSessionLocal
from backend.logger import setup_logger

logger = setup_logger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24


def hash_password(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain password against a bcrypt hash."""
    return pwd_context.verify(plain, hashed)


def create_access_token(subject: str, role: str, name: str) -> str:
    """Generate a signed JWT token with role and expiry."""
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": subject,       # employee_id or agent_id
        "role": role,         # "employee" or "agent"
        "name": name,         # display name
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and verify a JWT token. Raises JWTError if invalid."""
    return jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])


async def login(email: str, password: str) -> dict | None:
    """
    Verify credentials against DB.
    Checks employees first, then agents.
    Returns token dict or None if invalid.
    """
    async with AsyncSessionLocal() as session:
        # Check employees table
        result = await session.execute(
            select(Employee).where(Employee.email == email.lower())
        )
        employee = result.scalar_one_or_none()

        if employee and employee.password_hash and verify_password(password, employee.password_hash):
            token = create_access_token(
                subject=employee.employee_id,
                role="employee",
                name=employee.name,
            )
            logger.info("Employee login: %s", employee.employee_id)
            return {
                "access_token": token,
                "token_type": "bearer",
                "role": "employee",
                "id": employee.employee_id,
                "name": employee.name,
            }

        # Check agents table
        result = await session.execute(
            select(Agent).where(Agent.email == email.lower())
        )
        agent = result.scalar_one_or_none()

        if agent and agent.password_hash and verify_password(password, agent.password_hash):
            token = create_access_token(
                subject=agent.agent_id,
                role="agent",
                name=agent.name,
            )
            logger.info("Agent login: %s", agent.agent_id)
            return {
                "access_token": token,
                "token_type": "bearer",
                "role": "agent",
                "id": agent.agent_id,
                "name": agent.name,
            }

    logger.warning("Failed login attempt for email: %s", email)
    return None