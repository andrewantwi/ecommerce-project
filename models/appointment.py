from pydantic import BaseModel
from sqlalchemy import Column, Integer,ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime


class Appointment(BaseModel):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    visit_date = Column(DateTime, default=datetime.utcnow)
    condition = Column(Text)

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")