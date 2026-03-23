from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from tortoise import fields as tortoise_fields
from tortoise.expressions import Q
from tortoise.models import Model

from common.schemas import CommonResponse
from core.config import settings
from db.model_orm import Item
from modules.site_ops import (
    build_ops_overview,
    get_all_feature_flags,
    is_feature_enabled,
    list_log_files,
    tail_log_file,
    update_feature_flag,
)

from .ops_schema import (
    GetOpsFeatureFlagsResponse,
    GetOpsLogFilesResponse,
    GetOpsLogTailResponse,
    GetOpsOverviewResponse,
    GetQueryableTablesApiResponse,
    GetQueryableTablesResponse,
    LogFileInfo,
    LogFileListData,
    LogTailData,
    OpsFeatureFlagListData,
    OpsFeatureFlagRecord,
    OpsOverviewData,
    QueryableTable,
    QueryableTableColumn,
    TableQueryRequest,
    TableQueryResponse,
    TableQueryResult,
    UpdateFeatureFlagRequest,
    UpdateFeatureFlagResponse,
)


OPS_ACCESS_PASSWORD = "1230.123"

QUERYABLE_TABLES: Dict[str, Type[Model]] = {
    "item": Item,
}

DEFAULT_HIDDEN_COLUMNS: Dict[str, set[str]] = {}

STRING_OPERATORS = ["eq", "ne", "contains", "startswith", "endswith", "in", "is_null"]
NUMERIC_OPERATORS = ["eq", "ne", "gt", "gte", "lt", "lte", "in", "is_null"]
ENUM_OPERATORS = ["eq", "ne", "contains", "startswith", "endswith", "in", "is_null"]
BOOLEAN_OPERATORS = ["eq", "ne", "is_null"]
DATETIME_OPERATORS = ["eq", "ne", "gt", "gte", "lt", "lte", "is_null"]
GENERIC_OPERATORS = ["eq", "ne", "is_null"]


def require_ops_password(x_ops_password: Optional[str] = Header(default=None, alias="X-Ops-Password")):
    if x_ops_password != OPS_ACCESS_PASSWORD:
        raise HTTPException(status_code=401, detail="运维密码错误")


router = APIRouter(dependencies=[Depends(require_ops_password)])


def _require_feature_enabled(key: str, message: str):
    if not is_feature_enabled(key):
        raise HTTPException(status_code=503, detail=message)


def _require_db_enabled():
    if not settings.DB_ENABLED:
        raise HTTPException(status_code=503, detail="数据库未启用，无法查询数据表")


def _is_string_field(field: tortoise_fields.base.Field) -> bool:
    return isinstance(field, (tortoise_fields.CharField, tortoise_fields.TextField))


def _field_type(field: tortoise_fields.base.Field) -> str:
    if getattr(field, "enum_type", None) is not None:
        return "enum"
    if isinstance(field, tortoise_fields.BooleanField):
        return "boolean"
    if isinstance(field, (tortoise_fields.IntField, tortoise_fields.BigIntField, tortoise_fields.SmallIntField,
                          tortoise_fields.FloatField, tortoise_fields.DecimalField)):
        return "number"
    if isinstance(field, tortoise_fields.DatetimeField):
        return "datetime"
    if isinstance(field, tortoise_fields.DateField):
        return "date"
    if isinstance(field, tortoise_fields.TimeField):
        return "time"
    if isinstance(field, tortoise_fields.JSONField):
        return "json"
    if _is_string_field(field):
        return "string"
    return "string"


def _field_operators(field: tortoise_fields.base.Field) -> List[str]:
    field_type = _field_type(field)
    if field_type == "string":
        return STRING_OPERATORS
    if field_type == "number":
        return NUMERIC_OPERATORS
    if field_type == "enum":
        return ENUM_OPERATORS
    if field_type == "boolean":
        return BOOLEAN_OPERATORS
    if field_type in {"datetime", "date", "time"}:
        return DATETIME_OPERATORS
    return GENERIC_OPERATORS


def _model_columns(model: Type[Model]) -> List[str]:
    backward_fk_fields = set(getattr(model._meta, "backward_fk_fields", set()) or set())
    return [field_name for field_name in model._meta.fields_map.keys() if field_name not in backward_fk_fields]


def _table_columns(model: Type[Model], table_name: str) -> List[QueryableTableColumn]:
    hidden_set = DEFAULT_HIDDEN_COLUMNS.get(table_name, set())
    columns: List[QueryableTableColumn] = []
    for field_name in _model_columns(model):
        field = model._meta.fields_map[field_name]
        columns.append(
            QueryableTableColumn(
                name=field_name,
                type=_field_type(field),
                nullable=bool(getattr(field, "null", False)),
                operators=_field_operators(field),
                hidden_by_default=field_name in hidden_set,
            )
        )
    return columns


def _get_model_by_table(table_name: str) -> Type[Model]:
    model = QUERYABLE_TABLES.get(table_name)
    if model is None:
        raise HTTPException(status_code=400, detail=f"unsupported table: {table_name}")
    return model


def _parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and value in {0, 1}:
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "y", "on"}:
            return True
        if lowered in {"0", "false", "no", "n", "off"}:
            return False
    raise HTTPException(status_code=400, detail=f"invalid boolean value: {value}")


def _parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str) or not value.strip():
        raise HTTPException(status_code=400, detail=f"invalid datetime value: {value}")
    text = value.strip()
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"invalid datetime value: {value}") from exc


def _parse_scalar_value(field: tortoise_fields.base.Field, value: Any) -> Any:
    field_type = _field_type(field)
    if value is None:
        return None
    if field_type == "number":
        if isinstance(field, (tortoise_fields.IntField, tortoise_fields.BigIntField, tortoise_fields.SmallIntField)):
            try:
                return int(value)
            except (TypeError, ValueError) as exc:
                raise HTTPException(status_code=400, detail=f"invalid integer value: {value}") from exc
        try:
            return float(value)
        except (TypeError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=f"invalid number value: {value}") from exc
    if field_type == "boolean":
        return _parse_bool(value)
    if field_type in {"datetime", "date", "time"}:
        return _parse_datetime(value)
    if field_type == "enum":
        enum_type = getattr(field, "enum_type", None)
        if enum_type and isinstance(enum_type, type) and issubclass(enum_type, Enum):
            try:
                return enum_type(value)
            except ValueError as exc:
                allowed = [str(item.value) for item in enum_type]
                raise HTTPException(status_code=400, detail=f"invalid enum value: {value}, allowed={allowed}") from exc
    return str(value) if _is_string_field(field) else value


def _parse_in_values(field: tortoise_fields.base.Field, value: Any) -> List[Any]:
    if isinstance(value, (list, tuple, set)):
        raw_values = list(value)
    elif isinstance(value, str):
        raw_values = [item.strip() for item in value.split(",") if item.strip()]
    else:
        raw_values = [value]
    if not raw_values:
        raise HTTPException(status_code=400, detail="operator in requires non-empty value")
    return [_parse_scalar_value(field, item) for item in raw_values]


def _build_filter_q(model: Type[Model], column: str, op: str, value: Any) -> Q:
    field = model._meta.fields_map.get(column)
    if field is None:
        raise HTTPException(status_code=400, detail=f"unknown column: {column}")
    if op not in _field_operators(field):
        raise HTTPException(status_code=400, detail=f"unsupported operator '{op}' for column '{column}'")

    if op == "is_null":
        want_null = True if value is None else _parse_bool(value)
        return Q(**{f"{column}__isnull": want_null})
    if op == "in":
        return Q(**{f"{column}__in": _parse_in_values(field, value)})
    if op == "contains":
        return Q(**{f"{column}__icontains": str(value or "")})
    if op == "startswith":
        return Q(**{f"{column}__istartswith": str(value or "")})
    if op == "endswith":
        return Q(**{f"{column}__iendswith": str(value or "")})

    parsed_value = _parse_scalar_value(field, value)
    if op == "eq":
        return Q(**{column: parsed_value})
    if op == "ne":
        return ~Q(**{column: parsed_value})
    if op == "gt":
        return Q(**{f"{column}__gt": parsed_value})
    if op == "gte":
        return Q(**{f"{column}__gte": parsed_value})
    if op == "lt":
        return Q(**{f"{column}__lt": parsed_value})
    if op == "lte":
        return Q(**{f"{column}__lte": parsed_value})

    raise HTTPException(status_code=400, detail=f"unsupported operator: {op}")


def _to_json_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, list):
        return [_to_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _to_json_value(item) for key, item in value.items()}
    return value


def _default_columns(table_name: str, model: Type[Model]) -> List[str]:
    hidden_set = DEFAULT_HIDDEN_COLUMNS.get(table_name, set())
    columns = [name for name in _model_columns(model) if name not in hidden_set]
    return columns or _model_columns(model)


def _default_order_column(columns: List[str]) -> str:
    for candidate in ("reported_at", "updated_at", "created_at", "id"):
        if candidate in columns:
            return candidate
    return columns[0]


@router.get("/overview", response_model=GetOpsOverviewResponse, summary="查看运维总览")
async def get_ops_overview():
    payload = await build_ops_overview()
    return CommonResponse(data=OpsOverviewData(**payload))


@router.get("/features", response_model=GetOpsFeatureFlagsResponse, summary="查看功能开关")
async def get_feature_flags():
    items = [OpsFeatureFlagRecord(**item) for item in get_all_feature_flags()]
    return CommonResponse(data=OpsFeatureFlagListData(items=items))


@router.put("/features/{feature_key}", response_model=UpdateFeatureFlagResponse, summary="更新功能开关")
async def put_feature_flag(feature_key: str, payload: UpdateFeatureFlagRequest):
    try:
        updated = update_feature_flag(feature_key, payload.enabled)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"未知功能开关: {feature_key}") from exc
    return CommonResponse(message="更新成功", data=OpsFeatureFlagRecord(**updated))


@router.get("/logs/list", response_model=GetOpsLogFilesResponse, summary="列出日志文件")
async def get_log_files():
    _require_feature_enabled("ops_logs", "日志查看功能当前已关闭")
    files = [LogFileInfo(**item) for item in list_log_files()]
    return CommonResponse(data=LogFileListData(files=files))


@router.get("/logs/tail", response_model=GetOpsLogTailResponse, summary="查看日志末尾内容")
async def get_log_tail(
    filename: str = Query(..., description="日志文件名"),
    lines: int = Query(default=200, ge=20, le=2000, description="返回最近多少行"),
    keyword: Optional[str] = Query(default=None, description="关键字过滤"),
):
    _require_feature_enabled("ops_logs", "日志查看功能当前已关闭")
    try:
        payload = tail_log_file(filename=filename, lines=lines, keyword=keyword)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"日志文件不存在: {exc}") from exc
    return CommonResponse(data=LogTailData(**payload))


@router.get("/db/tables", response_model=GetQueryableTablesApiResponse, summary="列出可查询数据表")
async def list_queryable_tables():
    _require_feature_enabled("ops_submissions", "数据库表查询功能当前已关闭")
    _require_db_enabled()

    tables: List[QueryableTable] = []
    for table_name, model in QUERYABLE_TABLES.items():
        tables.append(QueryableTable(name=table_name, columns=_table_columns(model, table_name)))
    return CommonResponse(data=GetQueryableTablesResponse(tables=tables))


@router.post("/db/query", response_model=TableQueryResponse, summary="按条件查询数据表")
async def query_table(payload: TableQueryRequest):
    _require_feature_enabled("ops_submissions", "数据库表查询功能当前已关闭")
    _require_db_enabled()

    table_name = payload.table.strip()
    model = _get_model_by_table(table_name)

    available_columns = _model_columns(model)
    for item in payload.filters:
        if item.column not in available_columns:
            raise HTTPException(status_code=400, detail=f"unknown column: {item.column}")

    if payload.select_columns:
        select_columns = [name for name in payload.select_columns if name]
        invalid = [name for name in select_columns if name not in available_columns]
        if invalid:
            raise HTTPException(status_code=400, detail=f"unknown columns in select_columns: {invalid}")
    else:
        select_columns = _default_columns(table_name, model)

    if not select_columns:
        raise HTTPException(status_code=400, detail="no selectable columns")

    if payload.order_by:
        order_by = payload.order_by
        if order_by not in available_columns:
            raise HTTPException(status_code=400, detail=f"unknown order_by column: {order_by}")
    else:
        order_by = _default_order_column(available_columns)

    filters = Q()
    for item in payload.filters:
        filters &= _build_filter_q(model, item.column, item.op, item.value)

    order_expr = f"-{order_by}" if payload.order_desc else order_by
    query = model.filter(filters).order_by(order_expr)
    total_count = await query.count()
    rows = await query.offset((payload.page - 1) * payload.page_size).limit(payload.page_size).values(*select_columns)
    normalized_rows = [{key: _to_json_value(value) for key, value in row.items()} for row in rows]

    return CommonResponse(
        data=TableQueryResult(
            table=table_name,
            columns=select_columns,
            rows=normalized_rows,
            total_count=total_count,
            page=payload.page,
            page_size=payload.page_size,
        )
    )
