from datetime import datetime
from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import SQLAlchemyError  # Import for handling SQL exceptions
from fastapi.encoders import jsonable_encoder

from core.setup import Base
from schemas.doctor import DoctorIn, DoctorUpdate


class Doctor(Base):
    __tablename__ = 'doctor'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    reviews = relationship('Review', back_populates='doctor')
    appointments = relationship("Appointment", back_populates="doctor")


    def __str__(self) -> str:
        return self.username


    @classmethod
    def get_doctors(cls, db: Session):
        logger.info(f"Model: Getting Doctors")
        return db.query(cls).all()

    @classmethod
    def get_doctor(cls, doctor_id: int, db: Session):
        logger.info(f"Model: Getting Doctor")

        return db.query(cls).filter(cls.id == doctor_id).first()

    @classmethod
    def validate_id(cls, doctor_id: int, db: Session):
        try:
            logger.info(f"Model: Validating Doctor ID: {doctor_id}")
            doctor = db.query(cls).filter(cls.id == doctor_id).first()
            if not doctor:
                logger.warning(f"Model: Doctor ID {doctor_id} not found")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Doctor not found')
            logger.info(f"Model: Doctor ID {doctor_id} validated successfully")
        except SQLAlchemyError as e:
            logger.error(f"Model: SQLAlchemy Error while validating Doctor ID {doctor_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    @classmethod
    def validate_email(cls, email: str, db: Session):
        try:
            if db.query(cls).filter(cls.email == email).first():
                logger.warning(f"Model: Email {email} already registered")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')
        except SQLAlchemyError as e:
            logger.error(f"Model: SQLAlchemy Error while validating email {email}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    @classmethod
    def validate_doctor(cls, doctor: DoctorIn, db: Session):
        try:
            cls.validate_email(doctor.email, db)
            cls.validate_password(doctor.password, db)
        except HTTPException as e:
            logger.error(f"Model: Validation failed for doctor {doctor.email}: {str(e)}")
            raise e  # Re-raise the HTTPException if validation fails

    @classmethod
    def create_doctor(cls, doctor: DoctorIn, db: Session):
        try:
            doctor_instance = cls(**doctor.model_dump())
            db.add(doctor_instance)
            db.commit()
            db.refresh(doctor_instance)
            logger.info(f"Model: Doctor created with ID {doctor_instance.id}")
            return doctor_instance
        except SQLAlchemyError as e:
            logger.error(f"Model: SQLAlchemy Error while creating doctor {doctor.username}: {str(e)}")
            db.rollback()  # Ensure the transaction is rolled back on error
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    @classmethod
    def update_doctor(cls, doctor_id: int, update_data: DoctorUpdate, db: Session):
        try:
            doctor = db.query(cls).filter(cls.id == doctor_id).first()
            if doctor is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
            doctor.username = update_data.username
            doctor.password = update_data.password
            db.commit()
            db.refresh(doctor)
            logger.info(f"Model: Doctor with ID {doctor_id} updated successfully")
            return doctor
        except SQLAlchemyError as e:
            logger.error(f"Model: SQLAlchemy Error while updating doctor with ID {doctor_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    @classmethod
    def delete_doctor(cls, doctor_id: int, db: Session):
        try:
            doctor = db.query(cls).filter(cls.id == doctor_id).first()
            print(jsonable_encoder(doctor),'doc obj')
            if doctor is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
            db.delete(doctor)
            db.commit()
            logger.info(f"Model: Doctor with ID {doctor_id} deleted successfully")
            return doctor
        except SQLAlchemyError as e:
            logger.error(f"Model: SQLAlchemy Error while deleting doctor with ID {doctor_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
