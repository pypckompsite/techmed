from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Session, select, func

from security import generate_secure_password, hash_password
from functions import *
from models import *
from database import engine, get_db
from security import credentials_exception

admin_router = APIRouter()


def strip_sensitive_user_data(user_data_list: dict, db: Session = Depends(get_db)):
    # Define the keys to keep
    keys_to_keep = ["id", "link_id", "email", "type_id"]

    # Create a new list to hold stripped data
    stripped_data_list = []

    for user_data in user_data_list:
        # Initialize a new dictionary for stripped data
        stripped_data = {}

        # Manually add allowed keys to the stripped_data dictionary
        stripped_data["id"] = user_data.id
        stripped_data["email"] = user_data.email
        stripped_data["mfa_type"] = user_data.mfa_type
        stripped_data["type"] = user_data.type.name

        # Append the stripped data to the list
        stripped_data_list.append(stripped_data)

    return stripped_data_list

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


# @admin_router.get("/patients", tags=["User Management"])
# def get_users(db: Session = Depends(get_db), payload: dict = Depends(get_my_info)) -> list:
#     """Retrieve a list of all registered users in the system"""
#
#     if not payload or payload["type"] != "Admin":
#         raise credentials_exception
#
#     return [{"message": "NOT IMPLEMENTED"}]
#     # stmt = select(Patient)
#     # patients = db.exec(stmt).all()
#     #
#     # #Strip sensitive data
#     # patients_stripped = strip_sensitive_patient_data(patients)
#     #
#     # return(patients_stripped)


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
        print(db)
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


@admin_router.get("/patients/{pesel}", tags=["DEV_NOT_FINAL"])
def get_patient_info_endpoint(pesel: str, db: Session = Depends(get_db), payload: dict = Depends(get_my_info)):
    """Fetch detailed information about a specific patient by their PESEL number"""

    if not payload or payload["type"] != "Admin":
        raise credentials_exception

# , func.count(Patient.appointments)
    stmt = select(Patient).where(Patient.PESEL == pesel)
    print(stmt)
    patient = db.exec(stmt).first()

    if not patient:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Patient not found")


    return patient

    id: int = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=32)
    middle_name: str | None = Field(max_length=32)
    last_name: str = Field(max_length=64)
    PESEL: str = Field(max_length=11)
    gender: str = Field(max_length=1)
    address: str = Field(max_length=255)
    phone_number: str = Field(max_length=16)

    appointments: List["Appointment"] = Relationship(back_populates="patient")
    prescriptions: List["Prescription"] = Relationship(
        back_populates="patient")  # List of prescriptions for the patient
    referrals: List[Referral] = Relationship(back_populates="patient")
    test_results: List[TestResult] = Relationship(back_populates="patient")

@admin_router.post("/patients/add", tags=["User Management"])
def create_new_user(new_user_data: NewPatient, db: Session = Depends(get_db), payload: dict = Depends(get_my_info)):
    """Create a new patient account and profile with the provided information."""

    if not payload or payload["type"] != "Admin":
        raise credentials_exception

    new_patient = Patient(first_name=new_user_data.first_name, middle_name=new_user_data.middle_name, last_name=new_user_data.last_name, PESEL=new_user_data.PESEL, gender=new_user_data.gender, address=new_user_data.address, phone_number=new_user_data.phone_number)
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    password: str = generate_secure_password()

    new_user = User(email=new_user_data.email, hashed_password=hash_password(password), type_id = 1, link_id=new_patient.id)

    db.add(new_user)
    db.commit()

    return None
