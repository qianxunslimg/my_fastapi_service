from __future__ import annotations

from fastapi import APIRouter

from common.schemas import CommonResponse
from modules.site_ops import get_site_runtime_payload

from .site_schema import GetSiteRuntimeResponse, SiteRuntimeData


router = APIRouter()


@router.get("/runtime", response_model=GetSiteRuntimeResponse, summary="查看站点运行配置")
async def get_site_runtime():
    payload = get_site_runtime_payload()
    return CommonResponse(data=SiteRuntimeData(**payload))
