from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn
from typing import Optional

class Settings(BaseSettings):

    # ======== Core Application Settings ========
    APP_NAME: str = "Blog API"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"

    # ======== Database Configuration ========
    DATABASE_URL: PostgresDsn
    DB_POOL_SIZE: int = Field(5, ge=1)
    DB_MAX_OVERFLOW: int = Field(10, ge=0)
    DB_ECHO: bool = False

    # ======== Security Settings ========
    SECRET_KEY: str = Field(..., min_length=32)
    ALLOWED_ORIGINS: list[str] = ["*"]
    TRUSTED_IPS: list[str] = ["127.0.0.1"]

    # ======== JWT Configuration ========
    JWT_ALGORITHM: str = Field("HS256", pattern="^(HS256|HS384|HS512)$")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, ge=1)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, ge=1)
    JWT_ISSUER: str = "blog-api-server"

    # ======== Password Hashing ========
    PASSWORD_HASH_ROUNDS: int = Field(12, ge=10, le=20)
    PASSWORD_MIN_LENGTH: int = Field(8, ge=6)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()