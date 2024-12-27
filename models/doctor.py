from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session

from core.setup import Base
from schemas.doctor import DoctorIn, DoctorUpdate


class Doctor(Base):
    __tablename__ = 'doctor'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(String, default=datetime.now().isoformat())

    reviews = relationship('Review', back_populates='doctor')

    def __str__(self) -> str:
        self.doctorname

    @staticmethod
    def extract_username(email: str):
        return email.split('@')[0]

    @classmethod
    def validate_id(cls, doctor_id: int, db: Session):
        if not db.query(cls).filter(cls.id == doctor_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Doctor not found')
        return True

    @classmethod
    def validate_password(cls, password: str, db: Session):
        if len(password) < 6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Password must be at least 6 characters')

    @classmethod
    def validate_email(cls, email: str, db: Session):
        if db.query(cls).filter(cls.email == email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Email already registered')

    @classmethod
    def validate_doctor(cls, doctor: DoctorIn, db: Session):
        cls.validate_email(doctor.email, db)
        cls.validate_password(doctor.password, db)
        return doctor

    @classmethod
    def get_doctors(cls, db: Session):
        return db.query(cls).all()

    @classmethod
    def get_doctor(cls, doctor_id: int, db: Session):
        return db.query(cls).filter(cls.id == doctor_id).first()

    @classmethod
    def create_doctor(cls, doctor: DoctorIn, db: Session):
        username = cls.extract_username(doctor.email)
        doctor = cls(**doctor.dict(), username=username)
        db.add(doctor)
        return doctor

    @classmethod
    def update_doctor(cls, doctor_id: int, update_data: DoctorUpdate, db: Session):
        doctor = db.query(cls).filter(cls.id == doctor_id).first()
        doctor.username = update_data.username
        doctor.password = update_data.password
        return doctor

    @classmethod
    def delete_doctor(cls, doctor_id: int, db: Session):
        doctor = db.query(cls).filter(cls.id == doctor_id).first()
        db.delete(doctor)
        return doctor
