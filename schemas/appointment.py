from datetime import datetime
from pydantic import BaseModel


class AppointmentIn(BaseModel):
    doctor_id: int
    patient_id: int
    condition: str


class AppointmentOut(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    condition: str
    created_on: datetime
    updated_on: datetime


class AppointmentUpdate(BaseModel):
    doctor_id: int
    patient_id: int
    condition: str
