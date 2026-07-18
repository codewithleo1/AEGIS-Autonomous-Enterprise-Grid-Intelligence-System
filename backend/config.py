from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Groq
    groq_api_key: str

    # API Security
    aegis_api_key: str

    # JWT Auth
    jwt_secret: str

    # Upstash Redis
    upstash_redis_rest_url: str
    upstash_redis_rest_token: str

    # Supabase PostgreSQL
    database_url: str

    # App
    app_env: str = "development"
    app_version: str = "1.0.0"
    groq_model: str = "llama-3.3-70b-versatile"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()