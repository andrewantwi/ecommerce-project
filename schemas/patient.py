from datetime import datetime

from pydantic import BaseModel


class PatientIn(BaseModel):
    email: str
    password: str


class PatientOut(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime


class PatientUpdate(BaseModel):
    username: str
    password: str
