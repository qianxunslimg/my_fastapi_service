from __future__ import annotations

import time

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class AccessLogMiddleware(BaseHTTPMiddleware):
    """Log request duration and expose it through a response header."""

    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = int((time.perf_counter() - start) * 1000)
            logger.warning("Request failed {} {} ({} ms)", request.method, request.url.path, duration_ms)
            raise

        duration_ms = int((time.perf_counter() - start) * 1000)
        response.headers["X-Process-Time-Ms"] = str(duration_ms)
        logger.info("{} {} -> {} ({} ms)", request.method, request.url.path, response.status_code, duration_ms)
        return response
