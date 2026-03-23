from __future__ import annotations

import logging
import sys
from pathlib import Path

from loguru import logger

from core.config import settings


class InterceptHandler(logging.Handler):
    """Redirect standard logging into loguru."""

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except Exception:
            level = record.levelno
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    """Configure console and file logging once for the whole app."""
    logger.remove()
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.add(
        sys.stdout,
        colorize=True,
        level=settings.LOG_LEVEL,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        ),
    )
    logger.add(
        log_dir / "site.log",
        level=settings.LOG_LEVEL,
        rotation="10 MB",
        retention="30 days",
        encoding="utf-8",
    )

    intercept = InterceptHandler()
    logging.basicConfig(
        handlers=[intercept],
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        force=True,
    )
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        logging.getLogger(name).handlers = [intercept]
        logging.getLogger(name).propagate = False


def log_banner(message, char="#", width=60, level="INFO"):
    line = char * width
    logger.log(level, line)
    logger.log(level, message)
    logger.log(level, line)
