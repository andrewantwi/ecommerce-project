from typing import List
from loguru import logger
import fastapi

from controller.doctor import DoctorController
from schemas.doctor import DoctorOut, DoctorIn, DoctorUpdate

doctor_router = fastapi.APIRouter(prefix="/doctors")


@doctor_router.get("/", response_model=List[DoctorOut])
async def get_doctors():
    logger.info("Getting all doctors")
    return DoctorController.get_doctors()


@doctor_router.get("/{doctor_id}", response_model=DoctorOut)
async def get_doctor(doctor_id: int):
    return DoctorController.get_doctor(doctor_id)


@doctor_router.post("/", response_model=DoctorOut)
async def create_doctor(doctor: DoctorIn):
    return DoctorController.create_doctor(doctor)


@doctor_router.put("/{doctor_id}", response_model=DoctorOut)
async def update_doctor(doctor_id: int, doctor: DoctorUpdate):
    return DoctorController.update_doctor(doctor_id, doctor)


@doctor_router.delete("/{doctor_id}", response_model=DoctorOut)
async def delete_doctor(doctor_id: int):
    return DoctorController.delete_doctor(doctor_id)
