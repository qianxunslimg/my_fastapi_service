from tortoise import Tortoise, fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise

DATABASE_URL = "mysql://user:password@db:3306/database"


async def init():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={"models": ["db.model_orm"]},
    )
    await Tortoise.generate_schemas()

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL
    },
    "apps": {
        "models": {
            "models": ["db.model_orm", "aerich.models"],
            "default_connection": "default",
        },
    },
}
