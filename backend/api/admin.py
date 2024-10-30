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


def strip_sensitive_user_data(user_data_list: dict, db: Session = Depends(get_db)):

    # Create a new list to hold stripped data
    stripped_data_list = []

    for user_data in user_data_list:
        # Initialize a new dictionary for stripped data
        stripped_data = {"id": user_data.id, "email": user_data.email, "mfa_type": user_data.mfa_type,
                         "type": user_data.type.name}

        # Append the stripped data to the list
        stripped_data_list.append(stripped_data)

    return stripped_data_list

def strip_sensitive_patient_data(patient_data: dict, db: Session = Depends(get_db)):
    # Define the keys to keep

    # Create a new list to hold stripped data

    # Initialize a new dictionary for stripped data
    stripped_data = {"first_name": patient_data.first_name, "middle_name": patient_data.middle_name,
                     "last_name": patient_data.last_name, "PESEL": patient_data.PESEL,
                     "gender": patient_data.gender}


    return stripped_data


@admin_router.get("/users", tags=["User Management"])
def get_users(db: Session = Depends(get_db), payload: dict = Depends(get_my_info)) -> list:
    """Retrieve a list of all registered users in the system"""

    if not payload or payload["type"] != "Admin":
        raise credentials_exception

    stmt = select(User)
    users = db.exec(stmt).all()

    #Strip sensitive data
    users_stripped = strip_sensitive_user_data(users)

    return(users_stripped)


def get_my_info_test() -> dict:
    # Example payload for demonstration, replace with actual logic
    return {"type": "Admin"}


@admin_router.get("/patients", tags=["User Management"])
def get_users(db: Session = Depends(get_db), payload: dict = Depends(get_my_info)) -> list:
    """Retrieve a list of all patients in the system"""

    if not payload or payload["type"] != "Admin":
        raise credentials_exception

    stmt = select(Patient)
    patients = db.exec(stmt).all()

    #Strip sensitive data
    patients_stripped = strip_sensitive_patient_data(patients)

    return(patients_stripped)


@admin_router.get("/doctors", tags=["User Management"])
def get_users(db: Session = Depends(get_db), payload: dict = Depends(get_my_info)) -> list:
    """Retrieve a list of all doctors in the system"""

    if not payload or payload["type"] != "Admin":
        raise credentials_exception

    stmt = select(Doctor)
    doctors = db.exec(stmt).all()

    return(doctors)

@admin_router.get("/users/{user_id}", tags=["User Management"])
def get_user_info_endpoint(user_id: int, db: Session = Depends(get_db), payload: dict = Depends(get_my_info)):
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


@admin_router.get("/patients/{pesel}", tags=["User Management"])
def get_patient_info_endpoint(pesel: str, db: Session = Depends(get_db), payload: dict = Depends(get_my_info)):
    """Fetch detailed information about a specific patient by their PESEL number"""

    if not payload or payload["type"] != "Admin":
        raise credentials_exception

# , func.count(Patient.appointments)
    stmt = select(Patient).where(Patient.PESEL == pesel)
    patient = db.exec(stmt).first()

    if not patient:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Patient not found")

    patient_stripped = strip_sensitive_patient_data(patient)

    return patient_stripped

@admin_router.get("/doctors/{license_number}", tags=["DEV_NOT_FINAL"])
def get_doctor_info_endpoint(license_number: str, db: Session = Depends(get_db), payload: dict = Depends(get_my_info)):
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

@admin_router.post("/patients/add", tags=["User Management"])
def create_new_patient(new_user_data: NewPatient, db: Session = Depends(get_db), payload: dict = Depends(get_my_info)):
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


@admin_router.post("/doctors/add", tags=["User Management"])
def create_new_doctor(new_doctor_data: NewDoctor, db: Session = Depends(get_db), payload: dict = Depends(get_my_info)):
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
                        speciality_id=new_doctor_data.speciality_id)
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

    return {"message": "Doctor created", "patient_doctor_password": password}