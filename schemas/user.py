from datetime import datetime

from pydantic import BaseModel


class UserIn(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime


class UserUpdate(BaseModel):
    username: str
    password: str
