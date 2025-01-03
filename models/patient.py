from datetime import datetime
from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import SQLAlchemyError  # Import for handling SQL exceptions
from fastapi.encoders import jsonable_encoder

from core.setup import Base
from schemas.patient import PatientIn, PatientUpdate


class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    reviews = relationship('Review', back_populates='patient')
    appointments = relationship("Appointment", back_populates="patient")

    def __str__(self) -> str:
        return self.username


    @classmethod
    def get_patients(cls, db: Session):
        logger.info(f"Model: Getting Patients")
        return db.query(cls).all()

    @classmethod
    def get_patient(cls, patient_id: int, db: Session):
        logger.info(f"Model: Getting Patient")

        return db.query(cls).filter(cls.id == patient_id).first()

    @classmethod
    def validate_id(cls, patient_id: int, db: Session):
        try:
            logger.info(f"Model: Validating Patient ID: {patient_id}")
            patient = db.query(cls).filter(cls.id == patient_id).first()
            if not patient:
                logger.warning(f"Model: Patient ID {patient_id} not found")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Patient not found')
            logger.info(f"Model: Patient ID {patient_id} validated successfully")
        except SQLAlchemyError as e:
            logger.error(f"Model: SQLAlchemy Error while validating Patient ID {patient_id}: {str(e)}")
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
    def validate_patient(cls, patient: PatientIn, db: Session):
        try:
            cls.validate_email(patient.email, db)
            cls.validate_password(patient.password, db)
        except HTTPException as e:
            logger.error(f"Model: Validation failed for patient {patient.email}: {str(e)}")
            raise e  # Re-raise the HTTPException if validation fails

    @classmethod
    def create_patient(cls, patient: PatientIn, db: Session):
        try:
            patient_instance = cls(**patient.model_dump())
            db.add(patient_instance)
            db.commit()
            db.refresh(patient_instance)
            logger.info(f"Model: Patient created with ID {patient_instance.id}")
            return patient_instance
        except SQLAlchemyError as e:
            logger.error(f"Model: SQLAlchemy Error while creating patient {patient.username}: {str(e)}")
            db.rollback()  # Ensure the transaction is rolled back on error
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    @classmethod
    def update_patient(cls, patient_id: int, update_data: PatientUpdate, db: Session):
        try:
            patient = db.query(cls).filter(cls.id == patient_id).first()
            if patient is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
            patient.username = update_data.username
            patient.password = update_data.password
            db.commit()
            db.refresh(patient)
            logger.info(f"Model: Patient with ID {patient_id} updated successfully")
            return patient
        except SQLAlchemyError as e:
            logger.error(f"Model: SQLAlchemy Error while updating patient with ID {patient_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    @classmethod
    def delete_patient(cls, patient_id: int, db: Session):
        try:
            patient = db.query(cls).filter(cls.id == patient_id).first()
            print(jsonable_encoder(patient),'doc obj')
            if patient is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
            db.delete(patient)
            db.commit()
            logger.info(f"Model: Patient with ID {patient_id} deleted successfully")
            return patient
        except SQLAlchemyError as e:
            logger.error(f"Model: SQLAlchemy Error while deleting patient with ID {patient_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
