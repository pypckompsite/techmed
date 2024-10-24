# DO NOT USE!
# Further commits will be provided with compatible DB

exit(1)
#
# import random
# import string
# from datetime import datetime, timedelta
# from sqlmodel import Session
# from faker import Faker
# from passlib.context import CryptContext
# import os
#
# from database import engine, init_db
# from models import *
#
#
#
#
#
# init_db()
# print("Adding data to db...")
# # Poplate tables
# with Session(engine) as session:
#
# # Section for dictionaries
#     try:
#         user_types = [
#             UserType(id=1, name="Admin"),
#             UserType(id=2, name="Doctor"),
#             UserType(id=3, name="Patient"),
#         ]
#         session.add_all(user_types)
#         session.commit()
#     except Exception as e:
#         print("Table UserType already exist")
#
#     try:
#         appointment_statuses = [
#             AppointmentStatus(id=1, name="Scheduled"),
#             AppointmentStatus(id=2, name="Completed"),
#             AppointmentStatus(id=3, name="Cancelled"),
#             AppointmentStatus(id=4, name="No Show"),
#             AppointmentStatus(id=5, name="In Progress"),
#         ]
#         session.add_all(appointment_statuses)
#         session.commit()
#     except Exception as e:
#         print("Table AppointmentStatus already exists")
#
#
# with Session(engine) as session:
#
# # Section for 'main' tables
#
#     # Users
#     users = [
#         User(email=f"user{i}@example.com", hashed_password=f"hashedpassword{i}", otp_secret=f"secret{i}",
#              webauthn_key=f"key{i}", type=(i % 3) + 1, link_id=(i % 3) + 1)
#         for i in range(1, 11)  # Create 10 users
#     ]
#     session.add_all(users)
#
#     # Patients
#     patients = [
#         Patient(first_name=f"PatientFirstName{i}", middle_name=f"PatientMiddleName{i % 5}",
#                 last_name=f"PatientLastName{i}", PESEL=f"{i:011}", gender=("M" if i % 2 == 0 else "F"),
#                 address=f"{i} Main St, City, Country", phone_number=f"{1234567890 + i}")
#         for i in range(1, 101)  # Create 100 patients
#     ]
#     session.add_all(patients)
#
#
#     # Doctors
#     specialties = [
#         DoctorSpeciality(name="Cardiology", description="Heart and cardiovascular system", code="CARD"),
#         DoctorSpeciality(name="Neurology", description="Brain and nervous system", code="NEUR"),
#         DoctorSpeciality(name="Orthopedics", description="Bones and muscles", code="ORTH"),
#     ]
#     session.add_all(specialties)
#
#     doctors = [
#         Doctor(first_name=f"DoctorFirstName{i}", middle_name=f"DoctorMiddleName{i % 3}",
#                last_name=f"DoctorLastName{i}", phone_number=f"555{1000 + i}",
#                license_number=f"D{1000 + i}", hire_date=f"2022-01-{i % 30 + 1:02}",
#                speciality=(i % len(specialties)) + 1)  # Use the index for specialty
#         for i in range(1, 11)  # Create 10 doctors
#     ]
#     session.add_all(doctors)
#
#     # Appointments
#     appointments = [
#         Appointment(date=datetime(2024, 1, i, 10 + i % 5, 0), status=(i % 3) + 1,
#                     doctor_id=(i % len(doctors)) + 1, patient_id=(i % len(patients)) + 1,
#                     reason="Reason for appointment", treatment_plan="Treatment plan",
#                     diagnosis="Diagnosis", recommendations="Recommendations")
#         for i in range(1, 21)  # Create 20 appointments
#     ]
#     session.add_all(appointments)
#
# # Section for N-to-N combination tables
#
#
# # Commit changes
#     session.commit()
#
#     print("Done")