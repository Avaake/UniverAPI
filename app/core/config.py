from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIPrefix(BaseModel):
    api_v1: str = "/api/v1"


class DBConfig(BaseModel):
    naming_convention = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
    url: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 50


class AuthJWTConfig(BaseSettings):
    algorithm: str = "HS256"
    secret_key: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: DBConfig
    auth_jwt: AuthJWTConfig


settings = Settings()
