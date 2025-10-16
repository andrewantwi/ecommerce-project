from pydantic import BaseModel

class CheckoutIn(BaseModel):
    email : str
    total_amount : int
    

