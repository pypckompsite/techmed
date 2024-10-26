# DO NOT USE!
# Further commits will be provided with compatible DB



from sqlmodel import create_engine, Session, SQLModel


from security import hash_password
from models import *


DATABASE_URL = "sqlite:///orm.db"
engine = create_engine(DATABASE_URL)

SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)




print("Adding data to db...")
# Poplate tables
with Session(engine) as session:

# Section for dictionaries
    try:
        user_types = [
            UserType(id=0, name="Unassigned"),
            UserType(id=1, name="Patient"),
            UserType(id=2, name="Doctor"),
            UserType(id=3, name="Admin"),
        ]
        session.add_all(user_types)
        session.commit()
    except Exception as e:
        print("Table UserType already exist")
        raise e

    try:
        appointment_statuses = [
            AppointmentStatus(id=1, name="Scheduled"),
            AppointmentStatus(id=2, name="In Progress"),
            AppointmentStatus(id=3, name="Completed"),
            AppointmentStatus(id=4, name="No Show"),
            AppointmentStatus(id=5, name="Cancelled"),
        ]
        session.add_all(appointment_statuses)
        session.commit()
    except Exception as e:
        print("Table AppointmentStatus already exists")
        raise e


with Session(engine) as session:

# Section for 'main' tables

    # Users
    users = [
        User(email=f"user{i}@example.com", hashed_password=hash_password("password"), type_id=1, link_id=1)
        for i in range(0, 10)  # Create 10 users
    ]
    session.add_all(users)

    # Patients
    patients = [
        Patient(first_name=f"PatientFirstName{i}", middle_name=f"PatientMiddleName{i % 5}",
                last_name=f"PatientLastName{i}", PESEL=f"{i:011}", gender=("M" if i % 2 == 0 else "F"),
                address=f"{i} Main St, City, Country", phone_number=f"{1234567890 + i}")
        for i in range(0, 100)  # Create 100 patients
    ]
    session.add_all(patients)


    # Doctors
    specialties = [
        DoctorSpeciality(name="Cardiology", description="Heart and cardiovascular system", code="CARD"),
        DoctorSpeciality(name="Neurology", description="Brain and nervous system", code="NEUR"),
        DoctorSpeciality(name="Orthopedics", description="Bones and muscles", code="ORTH"),
    ]
    session.add_all(specialties)

    doctors = [
        Doctor(first_name=f"DoctorFirstName{i}", middle_name=f"DoctorMiddleName{i % 3}",
               last_name=f"DoctorLastName{i}", phone_number=f"555{1000 + i}",
               license_number=f"D{1000 + i}", hire_date=f"2022-01-{i % 30 + 1:02}",
               speciality_id=(i % len(specialties)) + 1)  # Use the index for specialty
        for i in range(1, 11)  # Create 10 doctors
    ]
    session.add_all(doctors)

    # Appointments
    appointments = [
        Appointment(date=datetime(2024, 1, i, 10 + i % 5, 0), status_id=(i % 3) + 1,
                    doctor_id=(i % len(doctors)) + 1, patient_id=(i % len(patients)) + 1,
                    reason="Reason for appointment", treatment_plan="Treatment plan",
                    diagnosis="Diagnosis", recommendations="Recommendations")
        for i in range(1, 21)  # Create 20 appointments
    ]
    session.add_all(appointments)

    drugs = [
        Drug(drug_id=1, name="Aspirin", form="Tablet", strength="500mg"),
        Drug(drug_id=2, name="Amoxicillin", form="Capsule", strength="250mg"),
        Drug(drug_id=3, name="Ibuprofen", form="Tablet", strength="200mg")
    ]
    session.add_all(drugs)

    prescriptions = [
        Prescription(
            prescription_id=i,
            doctor_id=(i % len(doctors)) + 1,  # Wybór lekarza na podstawie i
            patient_id=(i % len(patients)) + 1,  # Wybór pacjenta na podstawie i
            issue_date=date(2023, 10, i % 30 + 1),  # Przykładowe daty wystawienia
            expiration_date=date(2023, 12, i % 30 + 1),  # Przykładowe daty ważności
            notes="Notes for prescription {}".format(i),  # Uwagi
            status=PrescriptionStatus.active if i % 2 == 0 else PrescriptionStatus.purchased  # Status na podstawie i
        )
        for i in range(1, 21)  # Tworzenie 20 recept
    ]
    prescription_items = [
        PrescriptionItem(
            item_id=i,
            prescription_id=(i % len(prescriptions)) + 1,  # Wybór recepty na podstawie i
            drug_id=(i % len(drugs)) + 1,  # Wybór leku na podstawie i
            dosage="Dosage for item {}".format(i),  # Przykładowe dawkowanie
            quantity=(i % 10) + 1  # Ilość na podstawie i (1-10)
        )
        for i in range(1, 61)  # Tworzenie 60 pozycji recept
    ]
    session.add_all(prescription_items)
    session.add_all(prescriptions)

    referrals = [
        Referral(
            referral_id=i,
            patient_id=(i % len(patients)) + 1,  # Wybór pacjenta na podstawie i
            doctor_id=(i % len(doctors)) + 1,    # Wybór lekarza na podstawie i
            issue_date=date(2023, 10, i % 30 + 1),  # Przykładowe daty wystawienia
            reason="Reason for referral {}".format(i)  # Powód skierowania
        )
        for i in range(1, 21)  # Tworzenie 20 skierowań
    ]
    session.add_all(referrals)

    # Generowanie danych testowych dla wyników badań
    test_results = [
        TestResult(
            test_result_id=i,
            referral_id=(i % len(referrals)) + 1,  # Wybór skierowania na podstawie i
            patient_id=referrals[(i % len(referrals))].patient_id,  # ID pacjenta związane z skierowaniem
            test_name="Test for referral {}".format(i),  # Nazwa badania
            result="Result for test {}".format(i),  # Wynik badania
            date_performed=date(2023, 10, (i % 30) + 1)  # Przykładowa data wykonania
        )
        for i in range(1, 61)  # Tworzenie 60 wyników badań
    ]
    session.add_all(test_results)


# Section for N-to-N combination tables


# Commit changes
    session.commit()

    print("Done")