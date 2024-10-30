from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from pycparser.ply.yacc import token
from pydantic import BaseModel
from sqlmodel import Session, select, func

from api.functions import *
from api.models import *
from api.database import engine, get_db
from api.security import credentials_exception


misc_router = APIRouter()


@misc_router.get("/get_doctor_specialities", tags=["misc"])
def get_doctor_specialities(db: Session = Depends(get_db), payload: dict = Depends(verify_token)):

    if not payload:
        raise credentials_exception

    stmt = select(DoctorSpeciality)
    specialities = db.exec(stmt).all()

    return specialities

@misc_router.get("/get_appointment_statuses", tags=["misc"])
def get_doctor_specialities(db: Session = Depends(get_db), payload: dict = Depends(verify_token)):

    if not payload:
        raise credentials_exception

    stmt = select(AppointmentStatus)
    statusses = db.exec(stmt).all()

    return statusses