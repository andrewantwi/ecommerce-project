
from datetime import datetime
from enums import DepartmentEnum
from pydantic import BaseModel


class DoctorIn(BaseModel):
    username: str
    department: DepartmentEnum
    speciality: str

class DoctorOut(BaseModel):
    id: int
    username: str
    department: DepartmentEnum
    speciality: str
    created_at: datetime
    updated_at: datetime


class DoctorUpdate(BaseModel):
    username: str | None
    department: DepartmentEnum | None
    speciality: str | None

