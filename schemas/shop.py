from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ShopIn(BaseModel):
    owner_id: int
    name: str


class ShopUpdate(BaseModel):
    name: Optional[str] = None



class ShopOut(ShopIn):
    id: int
    owner_id: int
    created_at: datetime
    updated_at : datetime

    class Config:
        from_attributes = True