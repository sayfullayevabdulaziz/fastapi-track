from typing import Union, List, Optional, Dict, Any

from pydantic import BaseSettings, PostgresDsn, validator, AnyHttpUrl, EmailStr
from pathlib import Path


class Settings(BaseSettings):
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    ASSETS: str = "/static/images/"
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    PROJECT_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: Union[int, str]
    DATABASE_NAME: str
    DB_POOL_SIZE = 83
    WEB_CONCURRENCY = 9
    POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 10  # 10 days

    SECRET_KEY: str

    ASYNC_DATABASE_URI: Optional[str]

    @validator("ASYNC_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            host=values.get("DATABASE_HOST"),
            port=str(values.get("DATABASE_PORT")),
            path=f"/{values.get('DATABASE_NAME') or ''}",
        )

    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    BACKEND_CORS_ORIGINS: Union[List[str], List[AnyHttpUrl]]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # EMAIL SETTINGS for (GOOGLE SMTP)

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 465
    MAIL_SERVER: str
    MAIL_FROM_NAME: str


    class Config:
        case_sensitive = True
        env_file = './.env'


settings = Settings()
