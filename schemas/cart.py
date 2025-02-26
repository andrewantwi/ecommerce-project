from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from schemas.cart_item import CartItemIn



class CartIn(BaseModel):
    user_id: int
    total_price: float


class CartOut(BaseModel):
    id: int
    user_id: int
    total_price: float
    cart_items: List[CartItemIn] = None

class CartUpdate(BaseModel):
    user_id: int
    total_price: float
    cart_items: List[CartItemIn] = None

