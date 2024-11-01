from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Session, select, func

from api.security import generate_secure_password, hash_password
from api.functions import *
from api.models import *
from api.database import engine, get_db
from api.security import credentials_exception
from api.schemas import *

admin_router = APIRouter()




@admin_router.get("/users",
                  tags=["User Management"],
                  response_model=List[UserStripped],
                  responses={
                      401: {
                          "description": "Auth error",
                          "model": ErrorSchema
                      }
                    }
                  )
def get_users(db: Session = Depends(get_db),
              payload: dict = Depends(get_my_info)) -> list:
    """Retrieve a list of all registered users in the system"""

    if not payload or payload["type"] != "Admin":
        raise credentials_exception

    stmt = select(User)
    users = db.exec(stmt).all()


    return(users)



@admin_router.get("/patients",
                  tags=["User Management"],
                  response_model=List[PatientStripped],
                  responses={
                      401: {
                          "description": "Auth error",
                          "model": ErrorSchema
                      }
                    }
                  )
def get_users(db: Session = Depends(get_db),
              payload: dict = Depends(get_my_info)) -> list:
    """Retrieve a list of all patients in the system"""

    if not payload or payload["type"] != "Admin":
        raise credentials_exception

    stmt = select(Patient)
    patients: list = db.exec(stmt).all()

    return patients


@admin_router.get("/doctors",
                  tags=["User Management"],
                  response_model=List[DoctorStripped],
                  responses={
                      401: {
                          "description": "Auth error",
                          "model": ErrorSchema
                      }
                  }
                  )
def get_users(db: Session = Depends(get_db),
              payload: dict = Depends(get_my_info)) -> list:
    """Retrieve a list of all doctors in the system"""

    if not payload or payload["type"] != "Admin":
        raise credentials_exception

    stmt = select(Doctor)
    doctors = db.exec(stmt).all()

    return doctors

@admin_router.get("/users/{user_id}",
                  tags=["User Management"],
                  response_model=Union[GetUserInfoResponseDoctor, GetUserInfoResponseAdmin, GetUserInfoResponsePatient],
                  responses={
                      401: {
                          "description": "Auth error",
                          "model": ErrorSchema
                      },
                      400: {
                          "description": "Bad Request",
                          "model": ErrorSchema
                      }
                  }
                  )
def get_user_info_endpoint(user_id: int,
                           db: Session = Depends(get_db),
                           payload: dict = Depends(get_my_info)):
    """Fetch detailed information about a specific user by their ID"""

    if not payload or payload["type"] != "Admin":
        raise credentials_exception

    stmt = select(User).where(User.id == user_id)
    user = db.exec(stmt).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")


    if user.type.name == "Patient":
        patient = db.query(Patient).where(Patient.id == user.link_id).first()

        if not patient:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Fatal DB error")
        return GetUserInfoResponsePatient(email=user.email, type=user.type.name, patient=patient)

    elif user.type.name == "Doctor":
        stmt = select(Doctor).where(Doctor.id == user.link_id)
        doctor = db.exec(stmt).first()

        if not doctor:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Fatal DB error")

        return GetUserInfoResponseDoctor(email=user.email, type=user.type.name, doctor=Doctor)

    elif user.type.name == "Admin":
        # stmt = select(Patient).where(Patient.id == user.link_id)
        # patient = db.exec(stmt).first()
        #
        # if not patient:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Fatal DB error")
        #
        # return {"email": user.email, "type": user.type.name, 'Patient': patient}
        return  GetUserInfoResponseAdmin(email=user.email, type=user.type.name)

    elif user.type.name == "Unassigned":

        return {"email": user.email, "type": user.type.name}

    else:
        return {"email": user.email, "type": "Other"}


@admin_router.get("/patients/{pesel}",
                  tags=["User Management"],
                  response_model=PatientStripped,
                  responses={
                      401: {
                          "description": "Auth error",
                          "model": ErrorSchema
                      },
                      400: {
                          "description": "Bad Request",
                          "model": ErrorSchema
                      }
                    }
                  )
def get_patient_info_endpoint(pesel: str,
                              db: Session = Depends(get_db),
                              payload: dict = Depends(get_my_info)):
    """Fetch detailed information about a specific patient by their PESEL number"""

    if not payload or payload["type"] != "Admin":
        raise credentials_exception

# , func.count(Patient.appointments)
    stmt = select(Patient).where(Patient.PESEL == pesel)
    patient = db.exec(stmt).first()

    if not patient:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Patient not found")

    return patient

@admin_router.get("/doctors/{license_number}",
                  tags=["User Management"],
                  response_model=DoctorStripped,
                  responses={
                      401: {
                          "description": "Auth error",
                          "model": ErrorSchema
                      },
                      400: {
                          "description": "Bad Request",
                          "model": ErrorSchema
                      }
                    }
                  )
def get_doctor_info_endpoint(license_number: str,
                             db: Session = Depends(get_db),
                             payload: dict = Depends(get_my_info)):
    """Fetch detailed information about a specific patient by their PESEL number"""

    if not payload or payload["type"] != "Admin":
        raise credentials_exception

# , func.count(Patient.appointments)
    stmt = select(Doctor).where(Doctor.license_number == license_number)
    doctor = db.exec(stmt).first()

    if not doctor:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doctor not found")

    output: dict = doctor.__dict__
    output["speciality"] = {"id": doctor.speciality.id, "name": doctor.speciality.name}


    return output

@admin_router.post("/patients/add",
                   status_code=status.HTTP_201_CREATED,
                   tags=["User Management"],
                   response_model=NewPatientResponse,
                   responses={
                       401: {
                           "description": "Auth error",
                           "model": ErrorSchema
                       },
                       400: {
                           "description": "Bad Request",
                           "model": ErrorSchema
                       }
                     }
                   )
def create_new_patient(new_user_data: NewPatient,
                       db: Session = Depends(get_db),
                       payload: dict = Depends(get_my_info)):
    """Create a new patient account and profile with the provided information."""

    if not payload or payload["type"] != "Admin":
        raise credentials_exception

    stmt = select(User).where(User.email == new_user_data.email)
    db_user = db.exec(stmt).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_patient = Patient(first_name=new_user_data.first_name,
                          middle_name=new_user_data.middle_name,
                          last_name=new_user_data.last_name,
                          PESEL=new_user_data.PESEL,
                          gender=new_user_data.gender,
                          address=new_user_data.address,
                          phone_number=new_user_data.phone_number)
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    password: str = generate_secure_password()

    new_user = User(email=new_user_data.email,
                    hashed_password=hash_password(password),
                    type_id = 1, # Patient
                    link_id=new_patient.id)

    db.add(new_user)
    db.commit()

    return {"message": "Patient created", "patient_temp_password": password}


@admin_router.post("/doctors/add",
                   status_code=status.HTTP_201_CREATED,
                   tags=["User Management"],
                   response_model=NewDoctorResponse,
                   responses={
                       401: {
                           "description": "Auth error",
                           "model": ErrorSchema
                       },
                       400: {
                           "description": "Bad Request",
                           "model": ErrorSchema
                       }
                    }
                   )
def create_new_doctor(new_doctor_data: NewDoctor,
                      db: Session = Depends(get_db),
                      payload: dict = Depends(get_my_info)):
    """Create a new doctor account and profile with the provided information."""

    if not payload or payload["type"] != "Admin":
        raise credentials_exception

    stmt = select(Doctor).where(Doctor.license_number == new_doctor_data.license_number)
    db_doctor = db.exec(stmt).first()
    stmt = select(User).where(User.email == new_doctor_data.email)
    db_user = db.exec(stmt).first()
    if db_doctor or db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_doctor = Doctor(first_name=new_doctor_data.first_name,
                        middle_name=new_doctor_data.middle_name,
                        last_name=new_doctor_data.last_name,
                        phone_number=new_doctor_data.phone_number,
                        license_number=new_doctor_data.license_number,
                        hire_date=new_doctor_data.hire_date,
                        speciality=new_doctor_data.speciality)
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    password: str = generate_secure_password()

    new_user = User(email=new_doctor_data.email,
                    hashed_password=hash_password(password),
                    type_id = 2,  # Doctor
                    link_id=new_doctor.id)

    db.add(new_user)
    db.commit()

    return {"message": "Doctor created", "doctor_temp_password": password}