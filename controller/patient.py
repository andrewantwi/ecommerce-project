from loguru import logger
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models.patient import Patient
from schemas.patient import PatientIn, PatientUpdate
from utils.session import SessionManager as DBSession

class PatientController:

    @staticmethod
    def get_patients():
        try:
            with DBSession() as db:
                logger.info("Controller: Fetching all patients")
                patients = db.query(Patient).all()
                patients_list = [patient.to_dict() for patient in patients]
                return patients_list
        except Exception as e:
            logger.error(f"Controller: Error fetching patients: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching patients")

    @staticmethod
    def get_patient_by_id(patient_id: int):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Fetching patient with ID: {patient_id}")
                patient = db.query(Patient).filter(Patient.id == patient_id).first()
                if not patient:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
                return patient.to_dict()
        except Exception as e:
            logger.error(f"Controller: Error fetching patient with ID {patient_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching patient")

    @staticmethod
    def create_patient(patient: PatientIn):
        try:
            with DBSession() as db:
                patient_instance = Patient(**patient.model_dump())
                db.add(patient_instance)
                db.commit()
                db.refresh(patient_instance)
                logger.info(f"Controller: Patient created with ID {patient_instance.id}")
                return patient_instance.to_dict()
        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while creating patient {patient.email}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    @staticmethod
    def update_patient(patient_id: int, update_data: PatientUpdate):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Updating patient with ID {patient_id}")
                patient = db.query(Patient).filter(Patient.id == patient_id).first()
                if not patient:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
                for key, value in update_data.model_dump(exclude_unset=True).items():
                    setattr(patient, key, value)
                db.commit()
                db.refresh(patient)
                return patient.to_dict()
        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while updating patient with ID {patient_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    @staticmethod
    def delete_patient(patient_id: int):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Deleting patient with ID {patient_id}")
                patient = db.query(Patient).filter(Patient.id == patient_id).first()
                if not patient:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
                db.delete(patient)
                db.commit()
                return {"message": "Patient deleted successfully"}
        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while deleting patient with ID {patient_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
