from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter

from core.config import get_time_zone, settings

from .system_schema import GetServiceHealthResponse, ServiceHealthData


router = APIRouter()


@router.get("/health", response_model=GetServiceHealthResponse, summary="查看服务状态")
async def get_service_health():
    return GetServiceHealthResponse(
        data=ServiceHealthData(
            name=settings.APP_NAME,
            version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT,
            api_prefix=settings.API_PREFIX,
            time_zone=settings.TIME_ZONE,
            db_enabled=settings.DB_ENABLED,
            response_at=datetime.now(tz=get_time_zone()),
        )
    )
