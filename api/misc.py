from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from pycparser.ply.yacc import token
from pydantic import BaseModel
from sqlmodel import Session, select, func

from security import generate_secure_password, hash_password
from functions import *
from models import *
from database import engine, get_db
from security import credentials_exception


misc_router = APIRouter()


@misc_router.get("/get_doctor_specialities", tags=["misc"])
def get_doctor_specialities(db: Session = Depends(get_db), payload: dict = Depends(verify_token)):

    if not payload:
        raise credentials_exception

    stmt = select(DoctorSpeciality)
    specialities = db.exec(stmt).all()

    return specialities
