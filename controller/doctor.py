from models.doctor import Doctor
from schemas.doctor import DoctorIn, DoctorUpdate
from utils.session import SessionManager as DBSession


class DoctorController:

    @staticmethod
    def get_doctors():
        with DBSession() as db:
            doctors = Doctor.get_doctors(db)
            return doctors

    @staticmethod
    def get_doctor(doctor_id: int):
        with DBSession() as db:
            doctor = Doctor.validate_id(doctor_id, db)
            return doctor

    @staticmethod
    def create_doctor(doctor: DoctorIn):
        with DBSession() as db:
            Doctor.validate_doctor(doctor, db)
            doctor = Doctor.create_doctor(doctor, db)
            db.commit()
            db.refresh(doctor)
            return doctor

    @staticmethod
    def update_doctor(doctor_id: int, update_data: DoctorUpdate):
        with DBSession() as db:
            Doctor.validate_id(doctor_id, db)
            doctor = Doctor.update_doctor(doctor_id, update_data, db)
            db.commit()
            db.refresh(doctor)
            return doctor

    @staticmethod
    def delete_doctor(doctor_id: int):
        with DBSession() as db:
            Doctor.validate_id(doctor_id, db)
            doctor = Doctor.delete_doctor(doctor_id, db)
            db.commit()
            return doctor
