from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Base schema (shared properties)
class ShopIn(BaseModel):
    owner_id: int
    name: str


# Schema for updating a shop
class ShopUpdate(BaseModel):
    name: Optional[str] = None

# Schema for returning a shop (response model)
class ShopOut(ShopIn):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True