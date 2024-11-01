from fastapi import HTTPException
from fastapi.params import Depends
from sqlmodel import select, Session
from starlette import status

from api.models import Doctor
from api.models import User, Patient
from api.schemas import PatientStripped, DoctorStripped
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

        return {"email": user.email, "type": user.type, 'patient': PatientStripped(first_name=patient.first_name, last_name=patient.last_name, middle_name=patient.middle_name, gender=patient.gender)}

    elif user.type == "Doctor":
        stmt = select(Doctor).where(Doctor.id == user.link_id)
        doctor = db.exec(stmt).first()

        if not doctor:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Fatal DB error")
        return {"email": user.email, "type": user.type, 'doctor': DoctorStripped(id=doctor.id, first_name=doctor.first_name, last_name=doctor.last_name, middle_name=doctor.middle_name, phone_number=doctor.phone_number, license_number=doctor.license_number, hire_date=doctor.hire_date, speciality=doctor.speciality, facilities=doctor.facilities)}

    elif user.type == "Admin":

        return {"email": user.email, "type": user.type, 'Admin': "UNIMPLEMENTED"}

    elif user.type == "Unassigned":

        return {"email": user.email, "type": user.type}

    else:
        return {"email": user.email, "type": "Other"}


