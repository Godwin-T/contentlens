import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Blog API"
    API_V1_STR: str = "/api/v1"

    DB_HOST: str = os.environ.get("DB_HOST", default="localhost")
    DB_PORT: int = os.environ.get("DB_PORT", default=5432)
    DB_USER: str = os.environ.get("DB_USER", default="postgres")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", default="postgres")
    DB_NAME: str = os.environ.get("DB_NAME", default="postgres")
    DB_TYPE: str = os.environ.get("DB_TYPE", default="postgresql")

    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", "sqlite:///..databases/blogposts.db"
    )

    # JWT settings
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # CORS settings
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    BASE_DIR: str = os.environ.get("DATABASE_URL", default="../databases")
    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()
