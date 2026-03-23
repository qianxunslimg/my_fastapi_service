from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field

from common.schemas import CommonResponse


class SiteFeatureFlag(BaseModel):
    key: str = Field(..., description="功能开关键")
    label: str = Field(..., description="显示名称")
    description: str = Field(..., description="功能说明")
    group: str = Field(..., description="所属分组")
    enabled: bool = Field(..., description="是否启用")
    public: bool = Field(default=True, description="是否公开给前台")
    updated_at: str = Field(..., description="最近更新时间")


class SiteRuntimeData(BaseModel):
    name: str = Field(..., description="站点名称")
    version: str = Field(..., description="站点版本")
    environment: str = Field(..., description="运行环境")
    feature_flags: List[SiteFeatureFlag] = Field(default_factory=list, description="公开功能开关")
    feature_map: Dict[str, bool] = Field(default_factory=dict, description="公开功能开关键值")


GetSiteRuntimeResponse = CommonResponse[SiteRuntimeData]
