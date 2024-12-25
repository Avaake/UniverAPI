from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from dotenv import load_dotenv
from typing import ClassVar


load_dotenv()


class APIPrefix(BaseModel):
    api_v1: str = "/api/v1"
    auth: str = "/auth"
    role: str = "/roles"


class DBConfig(BaseModel):
    naming_convention: ClassVar[dict] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 50


class AuthJWTConfig(BaseSettings):
    algorithm: str = "HS256"
    secret_key: str
    access_token_expire_day: int = 15
    refresh_token_expire_day: int = 40


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: DBConfig
    auth_jwt: AuthJWTConfig
    api_prefix: APIPrefix = APIPrefix()


settings = Settings()
