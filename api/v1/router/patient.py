from typing import List
from loguru import logger
import fastapi

from controller.patient import PatientController
from schemas.patient import PatientOut, PatientIn, PatientUpdate

patient_router = fastapi.APIRouter(prefix="/patients")


@patient_router.get("/", response_model=List[PatientOut])
async def get_patients():
    logger.info("Router: Getting all patients")
    return PatientController.get_patients()


@patient_router.get("/{patient_id}", response_model=PatientOut)
async def get_patient(patient_id: int):
    logger.info(f"Router: Getting Patient with ID: {patient_id}")

    return PatientController.get_patient(patient_id)


@patient_router.post("/", response_model=PatientOut)
async def create_patient(patient: PatientIn):
    return PatientController.create_patient(patient)


@patient_router.put("/{patient_id}", response_model=PatientOut)
async def update_patient(patient_id: int, patient: PatientUpdate):
    return PatientController.update_patient(patient_id, patient)


@patient_router.delete("/{patient_id}", response_model=PatientOut)
async def delete_patient(patient_id: int):
    return PatientController.delete_patient(patient_id)
