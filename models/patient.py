
from fastapi import HTTPException, status
from loguru import logger
import json
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi.encoders import jsonable_encoder
from core.setup import Base
from schemas.patient import PatientIn, PatientUpdate
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




    @classmethod
    def get_patients(cls, db: Session):
        logger.info(f"Model: Getting Patients")
        patients: list[Patient] = db.query(cls).all() # type: ignore
        patients_list = [patient.to_dict() for patient in patients]
        logger.info(f"Model: Fetched Patients ==-> {patients_list}")
        return patients

    @classmethod
    def get_patient(cls, patient_id: int, db: Session):
        logger.info(f"Model: Getting Patient with ID: {patient_id}")
        patient = db.query(cls).filter(cls.id == patient_id).first()
        patient_str = json.dumps(patient)
        logger.info(f"Model: Fetched Patient with ID: {patient_id} ==-> {patient_str}")

        return patient



    @classmethod
    def create_patient(cls, patient: PatientIn, db: Session):
        try:
            patient_instance = cls(**patient.model_dump())
            logger.info(f"Model: Patient instance with ID {patient_instance}")
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
            for key, value in update_data.model_dump(exclude_unset=True).items():
                setattr(patient, key, value)
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
