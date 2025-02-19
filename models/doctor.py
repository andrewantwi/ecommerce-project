from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship
from core.setup import Base
from enums import DepartmentEnum


class Doctor(Base):
    __tablename__ = 'doctor'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=False)
    department = Column(Enum(DepartmentEnum), unique=False)
    speciality = Column(String, unique=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    reviews = relationship('Review', back_populates='doctor')
    appointments = relationship("Appointment", back_populates="doctor")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "department": str(self.department.name.lower()),
            "speciality": self.speciality,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
