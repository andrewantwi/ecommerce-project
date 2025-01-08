from datetime import datetime

from pydantic import BaseModel


class PatientIn(BaseModel):
    username: str
    email: str


class PatientOut(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    updated_at: datetime


class PatientUpdate(BaseModel):
    username: str
    email: str

