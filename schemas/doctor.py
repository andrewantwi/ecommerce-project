from datetime import datetime

from pydantic import BaseModel


class DoctorIn(BaseModel):
    email: str
    password: str


class DoctorOut(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime


class DoctorUpdate(BaseModel):
    username: str
    password: str
