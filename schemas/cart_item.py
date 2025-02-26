from pydantic import BaseModel, conint



class CartItemIn(BaseModel):
    product_id: int
    user_id: int
    price: float
    quantity: conint(ge=1)  # Ensure quantity is at least 1

class CartItemCreate(CartItemIn):
    pass

class CartItemUpdate(BaseModel):
    quantity: conint(ge=1)

class CartItemOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    price: float
    total_price: float

    class Config:
        from_attributes = True