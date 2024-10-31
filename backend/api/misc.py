from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.functions import *
from api.models import *
from api.database import get_db
from api.security import credentials_exception

from api.insert_mock_data import *

misc_router = APIRouter()


@misc_router.get("/get_doctor_specialities", tags=["misc"])
def get_doctor_specialities(db: Session = Depends(get_db), payload: dict = Depends(verify_token)):

    if not payload:
        raise credentials_exception

    stmt = select(DoctorSpeciality)
    specialities = db.exec(stmt).all()

    return specialities

@misc_router.get("/get_appointment_statuses", tags=["DEV"])
def get_appointment_statuses(db: Session = Depends(get_db), payload: dict = Depends(verify_token)):

    if not payload:
        raise credentials_exception

    appointment_status_json = [
        {"id": member.name, "name": member.value}
        for member in AppointmentStatus
    ]


    return appointment_status_json


@misc_router.get("/reset_db", tags=["misc"])
def reset_db():
    insert_mock_data()