from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

from database import engine


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
    middle_name: str = Field(max_length=32)
    last_name: str = Field(max_length=64)
    PESEL: str = Field(max_length=11)
    gender: str = Field(max_length=1)
    address: str = Field(max_length=255)
    phone_number: str = Field(max_length=16)

    appointments: list["Appointment"] = Relationship(back_populates="patient")

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
    appointments: list["Appointment"] = Relationship(back_populates="doctor")

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



