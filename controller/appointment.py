from loguru import logger
from fastapi import HTTPException, status

from models.appointment import Appointment
from schemas.appointment import AppointmentIn, AppointmentUpdate
from utils.session import SessionManager as DBSession


class AppointmentController:

    @staticmethod
    def get_appointments():
        try:
            with DBSession() as db:
                appointments = Appointment.get_appointments(db)
                return appointments
        except Exception as e:
            logger.error(f"Controller: Error fetching appointments: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching appointments")

    @staticmethod
    def get_appointment(appointment_id: int):
        try:
            with DBSession() as db:
                logger.info(f"Controller: Getting Appointment with ID: {appointment_id}")
                appointment = Appointment.get_appointment(appointment_id, db)
                if appointment is None:
                    logger.warning(f"Controller: Appointment with ID {appointment_id} not found")
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
                logger.info(f"Controller: Appointment found {appointment}")
                return appointment
        except HTTPException as e:
            logger.warning(f"Controller: {str(e.detail)}")
            raise e  # Re-raise the exception if it's an HTTPException
        except Exception as e:
            logger.error(f"Controller: Error fetching appointment with ID {appointment_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching appointment")

    @staticmethod
    def create_appointment(appointment: AppointmentIn):
        try:
            with DBSession() as db:
                appointment_instance = Appointment.create_appointment(appointment, db)
                db.commit()
                db.refresh(appointment_instance)
                logger.info(f"Controller: Appointment created with ID {appointment_instance.id}")
                return appointment_instance
        except HTTPException as e:
            logger.error(f"Controller: Validation failed for appointment  {str(e.detail)}")
            raise e  # Re-raise the exception if it's an HTTPException
        except Exception as e:
            logger.error(f"Controller: Error creating appointment: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating appointment")

    @staticmethod
    def update_appointment(appointment_id: int, update_data: AppointmentUpdate):
        try:
            with DBSession() as db:
                Appointment.validate_id(appointment_id, db)
                appointment = Appointment.update_appointment(appointment_id, update_data, db)
                db.commit()
                db.refresh(appointment)
                logger.info(f"Controller: Appointment with ID {appointment_id} updated")
                return appointment
        except HTTPException as e:
            logger.error(f"Controller: Appointment with ID {appointment_id} not found: {str(e.detail)}")
            raise e
        except Exception as e:
            logger.error(f"Controller: Error updating appointment with ID {appointment_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating appointment")

    @staticmethod
    def delete_appointment(appointment_id: int):
        try:
            with DBSession() as db:
                Appointment.validate_id(appointment_id, db)
                appointment = Appointment.delete_appointment(appointment_id, db)
                db.commit()
                logger.info(f"Controller: Appointment with ID {appointment_id} deleted")
                return appointment
        except HTTPException as e:
            logger.error(f"Controller: Appointment with ID {appointment_id} not found: {str(e.detail)}")
            raise e
        except Exception as e:
            logger.error(f"Controller: Error deleting appointment with ID {appointment_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting appointment")
