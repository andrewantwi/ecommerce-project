from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import SQLAlchemyError  # Import for handling SQL exceptions
from fastapi.encoders import jsonable_encoder
from core.setup import Base
from schemas.appointment import AppointmentIn, AppointmentOut, AppointmentUpdate


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    doctor_id = Column(Integer, ForeignKey("doctor.id"))
    condition = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")


    @classmethod
    def get_appointments(cls, db: Session):
        logger.info("Model: Getting Appointments")
        appointments = db.query(cls).all()
        logger.info(f"Model: Fetched Appointments : {appointments}")
        return appointments

    @classmethod
    def get_appointment(cls, appointment_id: int, db: Session):
        logger.info(f"Model: Getting Appointment with ID: {appointment_id}")
        appointment = db.query(cls).filter(cls.id == appointment_id).first()
        logger.info(f"Model: Fetched Appointment with ID: {appointment_id} ==-> {appointment}")

        return appointment



    @classmethod
    def create_appointment(cls, appointment: AppointmentIn, db: Session):
        try:
            appointment_instance = cls(**appointment.model_dump())
            logger.info(f"Model: Appointment instance with ID {appointment_instance}")
            db.add(appointment_instance)
            db.commit()
            db.refresh(appointment_instance)
            logger.info(f"Model: Appointment created with ID {appointment_instance.id}")
            return appointment_instance
        except SQLAlchemyError as e:
            logger.error(f"Model: SQLAlchemy Error while creating appointment : {str(e)}")
            db.rollback()  # Ensure the transaction is rolled back on error
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    @classmethod
    def update_appointment(cls, appointment_id: int, update_data: AppointmentUpdate, db: Session):
        try:
            appointment = db.query(cls).filter(cls.id == appointment_id).first()
            if appointment is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
            for key, value in update_data.model_dump(exclude_unset=True).items():
                setattr(appointment, key, value)
            db.commit()
            db.refresh(appointment)
            logger.info(f"Model: Appointment with ID {appointment_id} updated successfully")
            return appointment
        except SQLAlchemyError as e:
            logger.error(f"Model: SQLAlchemy Error while updating appointment with ID {appointment_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    @classmethod
    def delete_appointment(cls, appointment_id: int, db: Session):
        try:
            appointment = db.query(cls).filter(cls.id == appointment_id).first()
            print(jsonable_encoder(appointment),'doc obj')
            if appointment is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
            db.delete(appointment)
            db.commit()
            logger.info(f"Model: Appointment with ID {appointment_id} deleted successfully")
            return appointment
        except SQLAlchemyError as e:
            logger.error(f"Model: SQLAlchemy Error while deleting appointment with ID {appointment_id}: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")