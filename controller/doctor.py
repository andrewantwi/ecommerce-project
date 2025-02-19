from loguru import logger
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from models.doctor import Doctor
from schemas.doctor import DoctorIn, DoctorUpdate
from utils.session import SessionManager as DBSession
from fastapi.encoders import jsonable_encoder


class DoctorController:

    @staticmethod
    def get_doctors():
        try:
            with DBSession() as db:
                logger.info("Controller: Fetching all doctors")
                doctors = db.query(Doctor).all()
                doctors_list = [doctor.to_dict() for doctor in doctors]
                logger.info(f"Controller: Fetched Doctors ==-> {doctors_list}")
                return doctors_list
        except Exception as e:
            logger.error(f"Controller: Error fetching doctors: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching doctors")

    @staticmethod
    def get_doctor_by_id(doctor_id: int):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Fetching doctor with ID {doctor_id}")
                doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
                if not doctor:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
                logger.info(f"Controller: Fetched Doctor ==-> {jsonable_encoder(doctor)}")
                return doctor.to_dict()
        except HTTPException as e:
            logger.error(f"Controller: Doctor with ID {doctor_id} not found")
            raise e
        except Exception as e:
            logger.error(f"Controller: Error fetching doctor with ID {doctor_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching doctor")

    @staticmethod
    def create_doctor(doctor: DoctorIn):
        try:
            with DBSession() as db:
                doctor_instance = Doctor(**doctor.model_dump())
                logger.info(f"Controller: Creating doctor: {doctor_instance}")
                db.add(doctor_instance)
                db.commit()
                db.refresh(doctor_instance)
                logger.info(f"Controller: Doctor created with ID {doctor_instance.id}")
                return doctor_instance.to_dict()
        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while creating doctor {doctor.username}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
        except Exception as e:
            logger.error(f"Controller: Error creating doctor: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating doctor")

    @staticmethod
    def update_doctor(doctor_id: int, update_data: DoctorUpdate):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Updating doctor with ID {doctor_id}")
                doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
                if not doctor:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

                for key, value in update_data.model_dump(exclude_unset=True).items():
                    setattr(doctor, key, value)
                db.commit()
                db.refresh(doctor)
                logger.info(f"Controller: Doctor with ID {doctor_id} updated")
                return doctor.to_dict()

        except SQLAlchemyError as e:
            logger.error(f"Controller: SQLAlchemy Error while updating doctor with ID {doctor_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
        except Exception as e:
            logger.error(f"Controller: Error updating doctor with ID {doctor_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating doctor")

    @staticmethod
    def delete_doctor(doctor_id: int):
        with DBSession() as db:
            logger.info(f"Controller: Deleting doctor with ID {doctor_id}")
            doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

            if not doctor:
                logger.error(f"Controller: Doctor with ID {doctor_id} not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Doctor with ID {doctor_id} not found"
                )

            try:
                db.delete(doctor)
                db.commit()
                logger.info(f"Controller: Doctor with ID {doctor_id} deleted")
                return {"message": f"Doctor with ID {doctor_id} deleted successfully"}
            except SQLAlchemyError as e:
                db.rollback()  # Rollback transaction in case of error
                logger.error(f"Controller: SQLAlchemy Error while deleting doctor with ID {doctor_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database error"
                )
            except Exception as e:
                db.rollback()
                logger.error(f"Controller: Unexpected error deleting doctor with ID {doctor_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error deleting doctor"
                )

