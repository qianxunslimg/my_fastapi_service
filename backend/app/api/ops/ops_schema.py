from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from common.schemas import CommonResponse

FilterOperator = Literal["eq", "ne", "contains", "startswith", "endswith", "gt", "gte", "lt", "lte", "in", "is_null"]


class OpsFeatureFlagRecord(BaseModel):
    key: str = Field(..., description="开关键")
    label: str = Field(..., description="名称")
    description: str = Field(..., description="说明")
    group: str = Field(..., description="所属分组")
    enabled: bool = Field(..., description="是否启用")
    public: bool = Field(..., description="是否公开")
    updated_at: str = Field(..., description="更新时间")


class OpsFeatureFlagListData(BaseModel):
    items: List[OpsFeatureFlagRecord] = Field(default_factory=list, description="功能开关列表")


class UpdateFeatureFlagRequest(BaseModel):
    enabled: bool = Field(..., description="目标状态")


class LogFileInfo(BaseModel):
    name: str = Field(..., description="文件名")
    size: int = Field(..., description="文件大小")
    modified: str = Field(..., description="修改时间")


class LogFileListData(BaseModel):
    files: List[LogFileInfo] = Field(default_factory=list, description="日志文件列表")


class LogTailData(BaseModel):
    file: str = Field(..., description="日志文件名")
    lines: List[str] = Field(default_factory=list, description="日志内容")
    total_lines: int = Field(..., description="总行数")
    matched_lines: int = Field(..., description="命中过滤条件的行数")


class QueryableTableColumn(BaseModel):
    name: str = Field(..., description="字段名")
    type: str = Field(..., description="字段类型")
    nullable: bool = Field(..., description="是否可为空")
    operators: List[str] = Field(..., description="支持的筛选操作")
    hidden_by_default: bool = Field(False, description="默认查询是否隐藏该字段")


class QueryableTable(BaseModel):
    name: str = Field(..., description="表名")
    columns: List[QueryableTableColumn] = Field(..., description="字段元数据")


class GetQueryableTablesResponse(BaseModel):
    tables: List[QueryableTable] = Field(default_factory=list, description="可查询表列表")


class TableQueryFilter(BaseModel):
    column: str = Field(..., description="字段名")
    op: FilterOperator = Field("eq", description="筛选操作")
    value: Optional[Any] = Field(None, description="筛选值")


class TableQueryRequest(BaseModel):
    table: str = Field(..., description="目标表名")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=200, description="每页数量")
    filters: List[TableQueryFilter] = Field(default_factory=list, description="过滤条件列表")
    order_by: Optional[str] = Field(None, description="排序字段")
    order_desc: bool = Field(True, description="是否倒序")
    select_columns: Optional[List[str]] = Field(None, description="返回字段列表，不传则返回默认字段")


class TableQueryResult(BaseModel):
    table: str = Field(..., description="目标表名")
    columns: List[str] = Field(..., description="返回字段列表")
    rows: List[Dict[str, Any]] = Field(..., description="查询结果")
    total_count: int = Field(..., description="总数")
    page: int = Field(..., description="页码")
    page_size: int = Field(..., description="每页数量")


class OpsOverviewData(BaseModel):
    service_name: str = Field(..., description="服务名称")
    service_version: str = Field(..., description="服务版本")
    environment: str = Field(..., description="环境")
    log_dir: str = Field(..., description="日志目录")
    db_enabled: bool = Field(..., description="数据库是否启用")
    log_files_count: int = Field(..., description="日志文件数量")
    enabled_features: int = Field(..., description="启用中的开关数")
    feature_count: int = Field(..., description="总开关数")
    recent_logs: List[LogFileInfo] = Field(default_factory=list, description="最近日志")


GetOpsOverviewResponse = CommonResponse[OpsOverviewData]
GetOpsFeatureFlagsResponse = CommonResponse[OpsFeatureFlagListData]
UpdateFeatureFlagResponse = CommonResponse[OpsFeatureFlagRecord]
GetOpsLogFilesResponse = CommonResponse[LogFileListData]
GetOpsLogTailResponse = CommonResponse[LogTailData]
GetQueryableTablesApiResponse = CommonResponse[GetQueryableTablesResponse]
TableQueryResponse = CommonResponse[TableQueryResult]
