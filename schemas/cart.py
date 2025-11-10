from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from schemas.cart_item import CartItemIn, CartItemOut


class CartIn(BaseModel):
    user_id: int
    total_price: Optional[float] = 0.0


class CartOut(BaseModel):
    id: int
    user_id: int
    total_price: float
    cart_items: List[CartItemOut] = None

class CartUpdate(BaseModel):
    user_id: int
    total_price: float
    cart_items: List[CartItemIn] = None

