from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from common.schemas import CommonResponse


class ServiceHealthData(BaseModel):
    name: str = Field(description="服务名称")
    version: str = Field(description="服务版本")
    environment: str = Field(description="运行环境")
    api_prefix: str = Field(description="API 前缀")
    time_zone: str = Field(description="服务时区")
    db_enabled: bool = Field(description="是否启用数据库")
    response_at: datetime = Field(description="响应时间")


GetServiceHealthResponse = CommonResponse[ServiceHealthData]
