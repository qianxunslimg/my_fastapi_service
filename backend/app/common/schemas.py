from __future__ import annotations

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T")


class CommonResponse(BaseModel, Generic[T]):
    status: int = Field(default=200, description="HTTP 状态码")
    message: str = Field(default="success", description="返回消息")
    data: Optional[T] = Field(default=None, description="返回数据")


AnyResponse = CommonResponse[Any]


class ErrorResponse(BaseModel):
    status: int = Field(default=400, description="HTTP 状态码")
    message: str = Field(default="unknown error", description="错误消息")
