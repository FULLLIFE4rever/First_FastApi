from functools import cached_property
from pathlib import Path

from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASS = "postgres"
DB_NAME = "postgres"

DB_ORM = "postgresql"
DB_DRIVER = DB_ORM + "+" + "asyncpg"

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_PORT: int

    DB_HOST: str
    DB_NAME: str

    SECRET_KEY: SecretStr
    SECRET_ALGORITHM: SecretStr

    REDIS_HOST: str
    REDIS_PORT: int

    SMTP_HOST: str
    SMTP_USER: EmailStr
    SMTP_PORT: int
    SMTP_PASS: str

    TEST_MODE: bool = False

    TEST_POSTGRES_PASSWORD: str | None = None
    TEST_POSTGRES_USER: str | None = None
    TEST_POSTGRES_PORT: int | None = None
    TEST_DB_HOST: str | None = None
    TEST_DB_NAME: str | None = None

    @cached_property
    def get_url(self):

        if self.TEST_MODE:
            self.POSTGRES_PASSWORD = self.TEST_POSTGRES_PASSWORD
            self.POSTGRES_USER = self.TEST_POSTGRES_USER
            self.POSTGRES_PORT = self.TEST_POSTGRES_PORT
            self.DB_HOST = self.TEST_DB_HOST
            self.DB_NAME = self.TEST_DB_NAME
        url = (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.DB_HOST}:"
            f"{self.POSTGRES_PORT}/{self.DB_NAME}"
        )
        return url

    @cached_property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    # model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
