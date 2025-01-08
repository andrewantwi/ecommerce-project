from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.setup import Base


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    review = Column(String)
    rating = Column(Integer)
    doctor_id = Column(Integer, ForeignKey('doctor.id', ondelete='CASCADE'))  # Corrected foreign key
    patient_id = Column(Integer, ForeignKey('patient.id', ondelete='CASCADE'))  # Corrected foreign key

    created_at = Column(String, default=datetime.now().isoformat())

    doctor = relationship('Doctor', back_populates='reviews')
    patient = relationship('Patient', back_populates='reviews')
