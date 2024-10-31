import re

from fastapi import HTTPException
from pydantic import BaseModel, field_validator, constr
from sqlmodel import SQLModel
from starlette import status
from typing import Optional, List
from datetime import datetime,date

from api.models import *


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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email address must be valid")
        return value


class UserRegistration(EmailMixin, PasswordMixin):
    pass


class ChangePassword(PasswordMixin):
    current_password: str

class PESELMixin(BaseModel):
    PESEL: str

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
    address: str = constr(max_length=255)


    @field_validator("first_name")
    def validate_first_name(cls, value):
        if not value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="First name cannot be empty.")
        if not all(
                c.isalpha() for c in value):  # Allowing letters
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="First name must contain only letters")
        if len(value) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="First name must be at most 50 characters long.")
        return value

    @field_validator("middle_name")
    def validate_middle_name(cls, value):
        if value and not all(c.isalpha() for c in value):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Middle name must contain only letters")
        if value and len(value) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Middle name must be at most 50 characters long.")
        return value

    @field_validator("last_name")
    def validate_last_name(cls, value):
        if not value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Last name cannot be empty.")
        if not all(c.isalpha() for c in value):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Last name must contain only letters")
        if len(value) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Last name must be at most 50 characters long.")
        return value

    @field_validator("address")
    def validate_address(cls, value):
        if not value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Address cannot be empty.")
        # Allow letters, digits, spaces, commas, periods, hyphens, and special characters
        if not re.match(r"^[\w\s,.'-]+$", value):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Address contains invalid characters.")
        if len(value) > 255:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Address must be at most 255 characters long.")
        return value


class NewDoctor(EmailMixin, PESELMixin, GenderMixin, PhoneNUmberMixin):
    first_name: constr(min_length=3, max_length=32)
    middle_name: Optional[constr(max_length=32)]
    last_name: constr(min_length=3, max_length=32)
    license_number: constr(min_length=5, max_length=5)
    hire_date: date
    speciality_id: int

    @field_validator("first_name")
    def validate_first_name(cls, value):
        if not value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="First name cannot be empty.")
        if not all(
                c.isalpha() for c in value):  # Allowing letters
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="First name must contain only letters")
        if len(value) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="First name must be at most 50 characters long.")
        return value

    @field_validator("middle_name")
    def validate_middle_name(cls, value):
        if value and not all(c.isalpha() for c in value):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Middle name must contain only letters")
        if value and len(value) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Middle name must be at most 50 characters long.")
        return value

    @field_validator("last_name")
    def validate_last_name(cls, value):
        if not value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Last name cannot be empty.")
        if not all(c.isalpha() for c in value):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Last name must contain only letters")
        if len(value) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Last name must be at most 50 characters long.")
        return value



class PatientStripped(SQLModel):
    first_name: str
    middle_name: str | None
    last_name: str
    gender: str

class UserStripped(SQLModel):
    id: int
    email: str
    mfa_type: str | None

    type: UserType

class DoctorStripped(SQLModel):
    first_name: str = Field(max_length=32)
    middle_name: str = Field(max_length=32)
    last_name: str = Field(max_length=64)
    phone_number: str = Field(max_length=16)
    license_number: str = Field(max_length=16)
    hire_date: str = Field(max_length=11)

    speciality: DoctorSpeciality = Relationship(back_populates="doctors")
    facilities: List[MedicalFacility] = Relationship(back_populates="doctors", link_model=DoctorFacilityAssociation)


class AppointmentWithPatient(SQLModel):
    date: datetime
    reason: Optional[str]
    diagnosis: Optional[str]
    status: AppointmentStatus
    patient: PatientStripped  # Include patient information in the response

