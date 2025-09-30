from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


# Base schema (shared fields)
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None


# Input schema (used for creating new categories)
class CategoryIn(CategoryBase):
    pass


# Update schema (all fields optional for partial updates)
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


# Output schema (includes DB-generated fields)
class CategoryOut(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True