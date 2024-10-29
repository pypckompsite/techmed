from dulwich.porcelain import status
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

    if user.type.name == "Patient":
        patient = db.query(Patient).where(Patient.id == user.link_id).first()

        if not patient:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Fatal DB error")
        return {"email": user.email, "type": user.type.name, 'Patient': patient}

    elif user.type.name == "Doctor":
        stmt = select(Doctor).where(Doctor.id == user.link_id)
        doctor = db.exec(stmt).first()

        if not doctor:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Fatal DB error")

        return {"email": user.email, "type": user.type.name, 'Doctor': Doctor}

    elif user.type.name == "Admin":
        # stmt = select(Patient).where(Patient.id == user.link_id)
        # patient = db.exec(stmt).first()
        #
        # if not patient:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Fatal DB error")
        #
        # return {"email": user.email, "type": user.type.name, 'Patient': patient}
        return {"email": user.email, "type": user.type.name, 'Admin': "UNIMPLEMENTED"}

    elif user.type.name == "Unassigned":

        return {"email": user.email, "type": user.type.name}

    else:
        return {"email": user.email, "type": "Other"}


