import asyncio

from loguru import logger

from db.db import check_database_connection


async def main() -> None:
    try:
        await check_database_connection()
    except Exception as exc:
        logger.exception("Database connection check failed: {}", exc)
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
