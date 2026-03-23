from typing import Optional

from pydantic import BaseModel, ConfigDict


class ItemData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: Optional[str] = None
    description: Optional[str] = None
