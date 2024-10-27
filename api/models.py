import re
from pyexpat.errors import messages

from fastapi import HTTPException
from pydantic import BaseModel, field_validator, constr
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime,date
from enum import Enum
from typing import Optional, List

from starlette import status
from websockets.sync.server import basic_auth

from database import engine

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

# DATA Models:

email_regex = r"^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$"
email_pattern = re.compile(email_regex, re.IGNORECASE)


with open("wordlist_pl.txt", 'r', encoding="utf-8") as file:
    weak_passwords_set = {line.strip() for line in file if line.strip()}


def validate_email(email: str) -> bool:
    return bool(email_pattern.fullmatch(email))

class PasswordMixin(BaseModel):
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 12:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="The password must be at least 12 characters long.")
        if value in weak_passwords_set:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This password is considered too weak")
        return value

class EmailMixin(BaseModel):
    email: str

    @field_validator("email")
    def validate_email(cls, value):

        if not validate_email(value):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email address")
        return value


class UserRegistration(EmailMixin, PasswordMixin):
    pass


class ChangePassword(PasswordMixin):
    current_password: str

class PESELMixin(BaseModel):
    PESEL: constr(min_length=11, max_length=11)

    @field_validator("PESEL")
    def validate_pesel(cls, value):
        if not value.isdigit():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PESEL must contain only digits.")

        if len(value) != 11:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PESEL must be exactly 11 digits long.")

        # PESEL weights
        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        checksum = sum(int(digit) * weight for digit, weight in zip(value[:-1], weights)) % 10
        checksum_digit = (10 - checksum) % 10

        if checksum_digit != int(value[-1]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid PESEL: checksum does not match.")

        return value

class GenderMixin(BaseModel):
    gender: constr(min_length=1, max_length=1)

    @field_validator("gender")
    def validate_gender(cls, value):
        if value not in ("M", "F", "O", "K", 'I'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Gender is invalid")
        return value


class PhoneNUmberMixin(BaseModel):
    phone_number: constr(min_length=3, max_length=16)

    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        if len(value) < 3:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number must be at least 3 characters long.")
        if not re.match(r"^(\d{3}|\d{9}|\+\d{1,3}[\s]?\d{9,})$", value):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Phone number must valid")
        return value

class NewPatient(EmailMixin, PESELMixin, GenderMixin, PhoneNUmberMixin):
    first_name: constr(min_length=3, max_length=32)
    middle_name: Optional[constr(max_length=32)]
    last_name: constr(min_length=3, max_length=32)
    address: str = Field(max_length=255)


    @field_validator("first_name")
    def validate_first_name(cls, value):
        if not value:
            raise ValueError("First name cannot be empty.")
        if not all(
                c.isalpha() or c in "' -." for c in value):  # Allowing letters, apostrophes, spaces, hyphens, and dots
            raise ValueError(
                "First name must contain only letters and valid characters (e.g., spaces, hyphens, apostrophes, dots).")
        if len(value) > 50:
            raise ValueError("First name must be at most 50 characters long.")
        return value

    @field_validator("middle_name")
    def validate_middle_name(cls, value):
        if value and not all(c.isalpha() or c in "' -." for c in value):
            raise ValueError(
                "Middle name must contain only letters and valid characters (e.g., spaces, hyphens, apostrophes, dots).")
        if value and len(value) > 50:
            raise ValueError("Middle name must be at most 50 characters long.")
        return value

    @field_validator("last_name")
    def validate_last_name(cls, value):
        if not value:
            raise ValueError("Last name cannot be empty.")
        if not all(c.isalpha() or c in "' -." for c in value):
            raise ValueError(
                "Last name must contain only letters and valid characters (e.g., spaces, hyphens, apostrophes, dots).")
        if len(value) > 50:
            raise ValueError("Last name must be at most 50 characters long.")
        return value

    @field_validator("address")
    def validate_address(cls, value):
        if not value:
            raise ValueError("Address cannot be empty.")
        # Allow letters, digits, spaces, commas, periods, hyphens, and special characters
        if not re.match(r"^[\w\s,.'-]+$", value):
            raise ValueError("Address contains invalid characters.")
        if len(value) > 255:
            raise ValueError("Address must be at most 255 characters long.")
        return value