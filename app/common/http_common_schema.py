from typing import List, Dict, Any
from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any

T = TypeVar('T')

class CommonResponse(BaseModel, Generic[T]):
    status: int = Field(default=200, description="HTTP status code")
    message: str = Field(default="success", description="HTTP status message")
    data: Optional[T] = Field(default=None, description="Response data")

AnyResponse = CommonResponse[Any]

class ErrorResponse(BaseModel):
    status: int = Field(default=400, description="HTTP status code")
    message: str = Field(default="unknown error", description="HTTP status message")