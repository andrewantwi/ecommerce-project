from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserUpdate(BaseModel):
    full_name: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_owner: Optional[bool] = False

class UserIn(UserUpdate):
    hashed_password: str  # Accept plain text password for signup, but hash before storing

class UserOut(UserUpdate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
