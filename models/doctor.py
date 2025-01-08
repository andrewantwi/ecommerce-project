from fastapi import HTTPException, status
from loguru import logger
import json
from sqlalchemy import Column, Integer, String, Enum, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import SQLAlchemyError  # Import for handling SQL exceptions
from fastapi.encoders import jsonable_encoder
from core.setup import Base
from enums import DepartmentEnum
from schemas.doctor import DoctorIn, DoctorUpdate


class Doctor(Base):
    __tablename__ = 'doctor'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=False)
    department = Column(Enum(DepartmentEnum), unique=False)
    speciality = Column(String, unique=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    reviews = relationship('Review', back_populates='doctor')
    appointments = relationship("Appointment", back_populates="doctor")


    def to_dict(self) -> dict:
        department = self.department
        return {
            "id": self.id,
            "username": self.username,
            "department": str(department.name.lower()),
            "speciality": self.speciality,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }




    @classmethod
    def get_doctors(cls, db: Session):
        logger.info(f"Model: Getting Doctors")
        doctors: list[Doctor] = db.query(cls).all() # type: ignore
        doctors_list = [doctor.to_dict() for doctor in doctors]
        logger.info(f"Model: Fetched Doctors ==-> {doctors_list}")
        return doctors

    @classmethod
    def get_doctor(cls, doctor_id: int, db: Session):
        logger.info(f"Model: Getting Doctor with ID: {doctor_id}")
        doctor = db.query(cls).filter(cls.id == doctor_id).first()
        doctor_str = json.dumps(doctor)
        logger.info(f"Model: Fetched Doctor with ID: {doctor_id} ==-> {doctor_str}")

        return doctor



    @classmethod
    def create_doctor(cls, doctor: DoctorIn, db: Session):
        try:
            doctor_instance = cls(**doctor.model_dump())
            logger.info(f"Model: Doctor instance with ID {doctor_instance}")
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
            for key, value in update_data.model_dump(exclude_unset=True).items():
                setattr(doctor, key, value)
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
