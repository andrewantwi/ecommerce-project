
from datetime import datetime
from enums import DepartmentEnum
from pydantic import BaseModel
from typing import List, Optional




class ProductIn(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    shop_id: Optional[int] = None
    price: float
    is_available: bool = True
    image_urls: List[str]


class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    shop_id: Optional[int] = None
    price: float
    is_available: bool = True
    image_urls: List[str]


class ProductUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    shop_id: Optional[int] = None
    price: float
    is_available: bool = True
    image_urls: List[str]


class HomepageProductsResponse(BaseModel):
    popular: List[ProductOut]
    trending: List[ProductOut]
    featured: List[ProductOut]
