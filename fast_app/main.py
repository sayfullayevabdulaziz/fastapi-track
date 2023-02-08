from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from fastapi_async_sqlalchemy import db
from sqlmodel import text
from starlette.middleware.cors import CORSMiddleware

from fast_app.api.v1.api import api_router as api_router_v1
from fast_app.core.config import settings

# Core Application Instance

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=settings.ASYNC_DATABASE_URI,
    engine_args={
        "echo": False,
        "pool_pre_ping": True,
        "pool_size": settings.POOL_SIZE,
        "max_overflow": 64,
    },
)

# Set all CORS origins enabled
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Set Up static file
app.mount("/static", StaticFiles(directory=settings.BASE_DIR / "static"), name="static")


async def add_postgresql_extension() -> None:
    async with db():
        query = text("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        return await db.session.execute(query)


class CustomException(Exception):
    http_code: int
    code: str
    message: str

    def __init__(self, http_code: int = None, code: str = None, message: str = None):
        self.http_code = http_code if http_code else 500
        self.code = code if code else str(self.http_code)
        self.message = message


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def on_startup():
    await add_postgresql_extension()
    print("startup fastapi")


# Add Routers
app.include_router(api_router_v1, prefix=settings.API_V1_STR)


# FOR LOCAL
# if __name__ == "__main__":
#     uvicorn.run("main:app", host='127.0.0.1', port=8080,
#                 log_level="info", reload=True)