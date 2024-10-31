from fastapi import HTTPException
from fastapi.params import Depends
from sqlmodel import select, Session
from starlette import status

from api.models import Doctor
from api.models import User, Patient
from api.security import verify_token, credentials_exception
from api.database import get_db


def get_my_info(payload: dict = Depends(verify_token), db: Session = Depends(get_db)) -> dict:
    email = payload['sub']

    stmt = select(User).where(User.email == email)
    user = db.exec(stmt).first()

    if not user:
        raise credentials_exception

    if user.type == "Patient":
        patient = db.query(Patient).where(Patient.id == user.link_id).first()

        if not patient:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Fatal DB error")
        return {"email": user.email, "type": user.type, 'patient': patient.id}

    elif user.type == "Doctor":
        stmt = select(Doctor).where(Doctor.id == user.link_id)
        doctor = db.exec(stmt).first()

        if not doctor:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Fatal DB error")
        return {"email": user.email, "type": user.type, 'doctor_id': doctor.id}

    elif user.type == "Admin":

        return {"email": user.email, "type": user.type, 'Admin': "UNIMPLEMENTED"}

    elif user.type == "Unassigned":

        return {"email": user.email, "type": user.type}

    else:
        return {"email": user.email, "type": "Other"}


