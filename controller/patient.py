from loguru import logger
from fastapi import HTTPException, status

from models.patient import Patient
from schemas.patient import PatientIn, PatientUpdate
from utils.session import SessionManager as DBSession


class PatientController:

    @staticmethod
    def get_patients():
        try:
            with DBSession() as db:
                patients = Patient.get_patients(db)
                return patients
        except Exception as e:
            logger.error(f"Controller: Error fetching patients: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching patients")

    @staticmethod
    def get_patient(patient_id: int):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Getting Patient with ID: {patient_id}")
                patient = Patient.get_patient(patient_id, db)
                if patient is None:
                    logger.warning(f"Controller: Patient with ID {patient_id} not found")
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
                logger.info(f"Controller: Patient found {patient}")
                return patient
        except HTTPException as e:
            logger.warning(f"Controller: {str(e.detail)}")
            raise e  # Re-raise the exception if it's an HTTPException
        except Exception as e:
            logger.error(f"Controller: Error fetching patient with ID {patient_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching patient")

    @staticmethod
    def create_patient(patient: PatientIn):
        try:
            with DBSession() as db:
                patient_instance = Patient.create_patient(patient, db)
                db.commit()
                db.refresh(patient_instance)
                logger.info(f"Controller: Patient created with ID {patient_instance.id}")
                return patient_instance
        except HTTPException as e:
            logger.error(f"Controller: Validation failed for patient {patient.email}: {str(e.detail)}")
            raise e  # Re-raise the exception if it's an HTTPException
        except Exception as e:
            logger.error(f"Controller: Error creating patient: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating patient")

    @staticmethod
    def update_patient(patient_id: int, update_data: PatientUpdate):
        try:
            with DBSession() as db:
                Patient.validate_id(patient_id, db)
                patient = Patient.update_patient(patient_id, update_data, db)
                db.commit()
                db.refresh(patient)
                logger.info(f"Controller: Patient with ID {patient_id} updated")
                return patient
        except HTTPException as e:
            logger.error(f"Controller: Patient with ID {patient_id} not found: {str(e.detail)}")
            raise e
        except Exception as e:
            logger.error(f"Controller: Error updating patient with ID {patient_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating patient")

    @staticmethod
    def delete_patient(patient_id: int):
        try:
            with DBSession() as db:
                Patient.validate_id(patient_id, db)
                patient = Patient.delete_patient(patient_id, db)
                db.commit()
                logger.info(f"Controller: Patient with ID {patient_id} deleted")
                return patient
        except HTTPException as e:
            logger.error(f"Controller: Patient with ID {patient_id} not found: {str(e.detail)}")
            raise e
        except Exception as e:
            logger.error(f"Controller: Error deleting patient with ID {patient_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting patient")
