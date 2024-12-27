from loguru import logger
from fastapi import HTTPException, status

from models.doctor import Doctor
from schemas.doctor import DoctorIn, DoctorUpdate
from utils.session import SessionManager as DBSession


class DoctorController:

    @staticmethod
    def get_doctors():
        try:
            with DBSession() as db:
                doctors = Doctor.get_doctors(db)
                return doctors
        except Exception as e:
            logger.error(f"Controller: Error fetching doctors: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching doctors")

    @staticmethod
    def get_doctor(doctor_id: int):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Getting Doctor with ID: {doctor_id}")
                doctor = Doctor.get_doctor(doctor_id, db)
                if doctor is None:
                    logger.warning(f"Controller: Doctor with ID {doctor_id} not found")
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
                logger.info(f"Controller: Doctor found {doctor}")
                return doctor
        except HTTPException as e:
            logger.warning(f"Controller: {str(e.detail)}")
            raise e  # Re-raise the exception if it's an HTTPException
        except Exception as e:
            logger.error(f"Controller: Error fetching doctor with ID {doctor_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching doctor")

    @staticmethod
    def create_doctor(doctor: DoctorIn):
        try:
            with DBSession() as db:
                Doctor.validate_doctor(doctor, db)
                doctor_instance = Doctor.create_doctor(doctor, db)
                db.commit()
                db.refresh(doctor_instance)
                logger.info(f"Controller: Doctor created with ID {doctor_instance.id}")
                return doctor_instance
        except HTTPException as e:
            logger.error(f"Controller: Validation failed for doctor {doctor.email}: {str(e.detail)}")
            raise e  # Re-raise the exception if it's an HTTPException
        except Exception as e:
            logger.error(f"Controller: Error creating doctor: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating doctor")

    @staticmethod
    def update_doctor(doctor_id: int, update_data: DoctorUpdate):
        try:
            with DBSession() as db:
                Doctor.validate_id(doctor_id, db)
                doctor = Doctor.update_doctor(doctor_id, update_data, db)
                db.commit()
                db.refresh(doctor)
                logger.info(f"Controller: Doctor with ID {doctor_id} updated")
                return doctor
        except HTTPException as e:
            logger.error(f"Controller: Doctor with ID {doctor_id} not found: {str(e.detail)}")
            raise e
        except Exception as e:
            logger.error(f"Controller: Error updating doctor with ID {doctor_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating doctor")

    @staticmethod
    def delete_doctor(doctor_id: int):
        try:
            with DBSession() as db:
                Doctor.validate_id(doctor_id, db)
                doctor = Doctor.delete_doctor(doctor_id, db)
                db.commit()
                logger.info(f"Controller: Doctor with ID {doctor_id} deleted")
                return doctor
        except HTTPException as e:
            logger.error(f"Controller: Doctor with ID {doctor_id} not found: {str(e.detail)}")
            raise e
        except Exception as e:
            logger.error(f"Controller: Error deleting doctor with ID {doctor_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting doctor")
