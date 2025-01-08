from typing import List
from loguru import logger
import fastapi

from controller.appointment import AppointmentController
from schemas.appointment import AppointmentOut, AppointmentIn, AppointmentUpdate

appointment_router = fastapi.APIRouter(prefix="/appointments")


@appointment_router.get("/", response_model=List[AppointmentOut])
async def get_appointments():
    logger.info("Router: Getting all appointments")
    a=  AppointmentController.get_appointments()
    print(a)
    return a


@appointment_router.get("/{appointment_id}", response_model=AppointmentOut)
async def get_appointment(appointment_id: int):
    logger.info(f"Router: Getting Appointment with ID: {appointment_id}")

    return AppointmentController.get_appointment(appointment_id)


@appointment_router.post("/", response_model=AppointmentOut)
async def create_appointment(appointment: AppointmentIn):
    return AppointmentController.create_appointment(appointment)


@appointment_router.put("/{appointment_id}", response_model=AppointmentOut)
async def update_appointment(appointment_id: int, appointment: AppointmentUpdate):
    return AppointmentController.update_appointment(appointment_id, appointment)


@appointment_router.delete("/{appointment_id}", response_model=AppointmentOut)
async def delete_appointment(appointment_id: int):
    return AppointmentController.delete_appointment(appointment_id)
