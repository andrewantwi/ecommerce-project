from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime


class CategoryIn(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

class CategoryOut(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    # image_url: Optional[HttpUrl] = None

class CategoryUpdate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

