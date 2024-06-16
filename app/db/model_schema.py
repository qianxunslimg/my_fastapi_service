from pydantic import BaseModel
from typing import List, Optional


class ItemData(BaseModel):
    id: str
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True
