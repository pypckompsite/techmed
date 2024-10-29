from pyexpat.errors import messages

from fastapi import HTTPException
from pydantic import BaseModel, field_validator, constr
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime,date
from enum import Enum
from typing import Optional, List

from starlette import status
from websockets.sync.server import basic_auth

from api.database import engine

#IMPORTANT: Database models

class PrescriptionStatus(str, Enum):
    active = "Active"
    purchased = "Purchased"
    canceled = "Canceled"


class FacilityType(str, Enum):
    HOSPITAL = "Hospital"
    CLINIC = "Clinic"
    LABORATORY = "Laboratory"
    PHARMACY = "Pharmacy"


class DoctorFacilityAssociation(SQLModel, table=True):
    __tablename__ = "doctor_facility_association"

    doctor_id: Optional[int] = Field(default=None, foreign_key="doctor.id", primary_key=True)
    facility_id: Optional[int] = Field(default=None, foreign_key="medical_facility.facility_id", primary_key=True)

class MedicalFacility(SQLModel, table=True):
    __tablename__ = "medical_facility"

    facility_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, description="Nazwa placówki medycznej")
    address: str = Field(max_length=255, description="Adres placówki")
    phone_number: str = Field(max_length=15, description="Numer telefonu placówki")
    facility_type: FacilityType = Field(description="Typ placówki (np. Szpital, Przychodnia)")
    website: Optional[str] = Field(default=None, description="Strona internetowa placówki")
    operating_hours: Optional[str] = Field(default=None, description="Godziny otwarcia placówki")

    doctors: List["Doctor"] = Relationship(back_populates="facilities", link_model=DoctorFacilityAssociation)



class AppointmentStatus(SQLModel, table=True):
    __tablename__ = "appointment_status"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=32)

    appointments: list["Appointment"] = Relationship(back_populates="status")

class UserType(SQLModel, table=True):
    __tablename__ = "user_type"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=32)

    users: list["User"] = Relationship(back_populates="type")

class DoctorSpeciality(SQLModel, table=True):
    __tablename__ = "doctor_speciality"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=128)
    description: str = Field(max_length=1024)
    code: str = Field(max_length=16)

    doctors: list["Doctor"] = Relationship(back_populates="speciality")

class Referral(SQLModel, table=True):
    __tablename__ = "referral"

    referral_id: Optional[int] = Field(default=None, primary_key=True)  # Unikalny identyfikator skierowania
    patient_id: int = Field(foreign_key="patient.id")  # ID pacjenta
    doctor_id: int = Field(foreign_key="doctor.id")  # ID lekarza, który wystawia skierowanie
    issue_date: date = Field(default=None)  # Data wystawienia skierowania
    reason: str = Field(default=None)  # Powód skierowania

    patient: Optional["Patient"] = Relationship(back_populates="referrals")  # Relacja do pacjenta
    doctor: Optional["Doctor"] = Relationship(back_populates="referrals")
    test_result: Optional["TestResult"] = Relationship(back_populates="referral")  # Relacja 1:1


class TestResult(SQLModel, table=True):
    __tablename__ = "test_result"

    test_result_id: Optional[int] = Field(default=None, primary_key=True)  # Unikalny identyfikator wyniku badania
    referral_id: int = Field(foreign_key="referral.referral_id")  # ID skierowania
    patient_id: int = Field(foreign_key="patient.id")  # ID pacjenta
    test_name: str = Field(default=None)  # Nazwa badania
    result: str = Field(default=None)  # Wynik badania
    date_performed: date = Field(default=None)  # Data wykonania badania

    referral: Optional[Referral] = Relationship(back_populates="test_result")  # Relacja 1:1 do skierowania
    patient: Optional["Patient"] = Relationship(back_populates="test_results")  # Relacja do pacjenta


class User(SQLModel, table=True):
    __tablename__ = "user"
    id: int = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True)
    hashed_password: str = Field(default="")
    mfa_type: str | None = Field(default=None)
    otp_secret: str | None = None
    webauthn_key: str | None = None
    type_id: int = Field(default=0, foreign_key="user_type.id")
    link_id: int | None = Field(default=None)

    type: UserType = Relationship(back_populates="users")

class Patient(SQLModel, table=True):
    __tablename__ = "patient"
    id: int = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=32)
    middle_name: str | None = Field(max_length=32)
    last_name: str = Field(max_length=64)
    PESEL: str = Field(max_length=11)
    gender: str = Field(max_length=1)
    address: str = Field(max_length=255)
    phone_number: str = Field(max_length=16)

    appointments: List["Appointment"] = Relationship(back_populates="patient")
    prescriptions: List["Prescription"] = Relationship(back_populates="patient")  # List of prescriptions for the patient
    referrals: List[Referral] = Relationship(back_populates="patient")
    test_results: List[TestResult] = Relationship(back_populates="patient")

class Doctor(SQLModel, table=True):
    __tablename__ = "doctor"
    id: int = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=32)
    middle_name: str = Field(max_length=32)
    last_name: str = Field(max_length=64)
    phone_number: str = Field(max_length=16)
    license_number: str = Field(max_length=16)
    hire_date: str = Field(max_length=11)
    speciality_id: int = Field(default=None, foreign_key="doctor_speciality.id")

    speciality: DoctorSpeciality = Relationship(back_populates="doctors")
    appointments: List["Appointment"] = Relationship(back_populates="doctor")
    prescriptions: List["Prescription"] = Relationship(back_populates="doctor")
    referrals: List[Referral] = Relationship(back_populates="doctor")
    facilities: List[MedicalFacility] = Relationship(back_populates="doctors", link_model=DoctorFacilityAssociation)

class Appointment(SQLModel, table=True):
    __tablename__ = "appointment"
    id: int = Field(default=None, primary_key=True)
    date: datetime = Field(default=None)
    status_id: int = Field(default=1, foreign_key="appointment_status.id")  # Ensure this refers to the correct AppointmentStatus table
    doctor_id: int = Field(foreign_key='doctor.id')
    patient_id: int = Field(foreign_key='patient.id')
    reason: str = Field(default=None)
    treatment_plan: str = Field(default=None)
    diagnosis: str = Field(default=None)
    recommendations: str = Field(default=None)

    status: AppointmentStatus = Relationship(back_populates="appointments")
    doctor: Doctor = Relationship(back_populates="appointments")
    patient: Patient = Relationship(back_populates="appointments")


class Prescription(SQLModel, table=True):
    __tablename__ = "prescription"
    prescription_id: int = Field(default=None, primary_key=True)  # Unique identifier for the prescription
    doctor_id: int = Field(foreign_key="doctor.id")  # Doctor's ID
    patient_id: int = Field(foreign_key="patient.id")  # Patient's ID
    issue_date: date = Field(default=None)  # Issue date
    expiration_date: date = Field(default=None)  # Expiration date
    notes: Optional[str] = Field(default=None)  # Doctor's notes
    status: PrescriptionStatus = Field(default=None)  # Prescription status

    doctor: Optional[Doctor] = Relationship(back_populates="prescriptions")     # Relationship to Doctor
    patient: Optional[Patient] = Relationship(back_populates="prescriptions")   # Relationship to Patient
    items: List["PrescriptionItem"] = Relationship(back_populates="prescriptions")  # Relationship to PrescriptionItem


class Drug(SQLModel, table=True):
    __tablename__ = "drug"
    drug_id: Optional[int] = Field(default=None, primary_key=True)  # Unique identifier for the drug
    name: str = Field(default=None)  # Drug name
    form: str = Field(default=None)  # Form of the drug
    strength: str = Field(default=None)  # Strength of the drug

    prescription_items: List["PrescriptionItem"] = Relationship(back_populates="drug")  # Relationship to PrescriptionItem

class PrescriptionItem(SQLModel, table=True):
    __tablename__ = "prescriptionitem"
    item_id: int = Field(default=None, primary_key=True)  # Unique identifier for the prescription item
    prescription_id: int = Field(foreign_key="prescription.prescription_id")  # ID of the prescription this item belongs to
    drug_id: int = Field(foreign_key="drug.drug_id") # Drug name
    dosage: str = Field(default=None)  # Drug dosage
    quantity: int = Field(default=None)  # Quantity of drug

    prescriptions: Optional[Prescription] = Relationship(back_populates="items")  # Relationship to Prescription table
    drug: Optional[Drug] = Relationship(back_populates="prescription_items")

