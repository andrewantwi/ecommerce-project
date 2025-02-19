
from sqlalchemy.orm import relationship
from core.setup import Base
from sqlalchemy import Column, Integer, String, Enum,DateTime, func



class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    reviews = relationship('Review', back_populates='patient')
    appointments = relationship("Appointment", back_populates="patient")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
