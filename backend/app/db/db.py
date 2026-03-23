from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from loguru import logger

from core.config import settings


DATABASE_URL = settings.DATABASE_URL


async def init():
    await connect_db()
    await Tortoise.generate_schemas()


async def connect_db():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={"models": ["db.model_orm"]},
        use_tz=True,
        timezone=settings.TIME_ZONE,
    )


async def close_db():
    await Tortoise.close_connections()


async def check_database_connection():
    if not settings.DB_ENABLED:
        logger.info("Skip database connection check because DB_ENABLED=false")
        return

    close_after = False
    try:
        if not getattr(Tortoise, "_inited", False):
            await connect_db()
            close_after = True
        connection = Tortoise.get_connection("default")
        await connection.execute_query("SELECT 1")
        logger.info("Database connection check succeeded")
    finally:
        if close_after:
            await close_db()


TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL,
    },
    "use_tz": True,
    "timezone": settings.TIME_ZONE,
    "apps": {
        "models": {
            "models": ["db.model_orm", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def register_db(app):
    if not settings.DB_ENABLED:
        return

    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=settings.DB_GENERATE_SCHEMAS,
        add_exception_handlers=True,
    )
