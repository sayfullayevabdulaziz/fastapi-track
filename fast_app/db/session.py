from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from fast_app.core.config import settings

DB_POOL_SIZE = 83
WEB_CONCURRENCY = 9
POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)


engine = create_async_engine(
    settings.ASYNC_DATABASE_URI,
    echo=True,
    future=True,
    pool_size=POOL_SIZE,
    max_overflow=64,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)