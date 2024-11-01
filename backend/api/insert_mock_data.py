# DO NOT USE!
# Further commits will be provided with compatible DB



from sqlmodel import create_engine, Session, SQLModel


from api.models import *


DATABASE_URL = "sqlite:///orm.db"
engine = create_engine(DATABASE_URL)






print("Adding data to db...")
# Poplate tables

def insert_mock_data():
    try:
        SQLModel.metadata.drop_all(engine)
    except:
        pass

    try:
        SQLModel.metadata.create_all(engine)
    except:
        pass

    with Session(engine) as session:

    # Section for 'main' tables

        # Users
        users = [
            User(email=f"user{i}@example.com", hashed_password="$argon2id$v=19$m=131072,t=25,p=4$1to7p7Q2Rqh1rnUOASDEuA$EajgMftTz5z5uXA9mK5RS/K/z7IhTV5Jel3qq27mVbAIx0bxhD/aGM0jhYlkLPqRJnc+6NyN//tHYJMBr4TJBg", type=UserType.Patient, link_id=1)
            for i in range(0, 10)  # Create 10 users
        ]
        admin = User(email=f"admin@example.com", hashed_password="$argon2id$v=19$m=131072,t=25,p=4$1to7p7Q2Rqh1rnUOASDEuA$EajgMftTz5z5uXA9mK5RS/K/z7IhTV5Jel3qq27mVbAIx0bxhD/aGM0jhYlkLPqRJnc+6NyN//tHYJMBr4TJBg", type=UserType.Admin, link_id=1)
        doctor = User(email=f"doctor@example.com", hashed_password="$argon2id$v=19$m=131072,t=25,p=4$1to7p7Q2Rqh1rnUOASDEuA$EajgMftTz5z5uXA9mK5RS/K/z7IhTV5Jel3qq27mVbAIx0bxhD/aGM0jhYlkLPqRJnc+6NyN//tHYJMBr4TJBg", type=UserType.Doctor, link_id=1)
        unassigned = User(email=f"unassigned@example.com", hashed_password="$argon2id$v=19$m=131072,t=25,p=4$1to7p7Q2Rqh1rnUOASDEuA$EajgMftTz5z5uXA9mK5RS/K/z7IhTV5Jel3qq27mVbAIx0bxhD/aGM0jhYlkLPqRJnc+6NyN//tHYJMBr4TJBg", type=UserType.Unassigned)
        users.append(admin)
        users.append(doctor)
        users.append(unassigned)
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
        appointments_scheduled = [
            Appointment(date=datetime(2024, 12, i, 10 + i % 5, 0), status=AppointmentStatus.SCHEDULED,
                        doctor_id=(i % len(doctors)) + 1, patient_id=(i % len(patients)) + 1,
                        reason="Reason for appointment", treatment_plan="Treatment plan",
                        diagnosis="Diagnosis", recommendations="Recommendations")
            for i in range(1, 21)  # Create 20 appointments
        ]

        appointments_canceled = [
            Appointment(date=datetime(2024, 10, i, 10 + i % 5, 0), status=AppointmentStatus.CANCELLED,
                        doctor_id=(i % len(doctors)) + 1, patient_id=(i % len(patients)) + 1,
                        reason="Reason for appointment", treatment_plan="Treatment plan",
                        diagnosis="Diagnosis", recommendations="Recommendations")
            for i in range(1, 21)  # Create 20 appointments
        ]

        appointments_completed = [
            Appointment(date=datetime(2024, 10, i, 10 + i % 5, 0), status=AppointmentStatus.COMPLETED,
                        doctor_id=(i % len(doctors)) + 1, patient_id=(i % len(patients)) + 1,
                        reason="Reason for appointment", treatment_plan="Treatment plan",
                        diagnosis="Diagnosis", recommendations="Recommendations")
            for i in range(1, 21)  # Create 20 appointments
        ]

        session.add_all(appointments_scheduled)
        session.add_all(appointments_canceled)
        session.add_all(appointments_completed)

        drugs = [
            Drug(drug_id=1, name="Aspirin", form="Tablet", strength="500mg", active_substance="acetylsalicylic acid"),
            Drug(drug_id=2, name="Amoxil", form="Capsule", strength="250mg", active_substance="Amoxicillin"),
            Drug(drug_id=3, name="Advil", form="Tablet", strength="200mg", active_substance="Ibuprofen"),
            Drug(drug_id=4, name="Ibuprofen", form="Tablet", strength="200mg", active_substance="Ibuprofen"),
            Drug(drug_id=5, name="Ibum", form="Tablet", strength="200mg", active_substance="Ibuprofen")
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

        facilities = [
            MedicalFacility(
                facility_id=1,
                name="General Hospital",
                address="123 Main St, Cityville",
                phone_number="123-456-7890",
                facility_type=FacilityType.HOSPITAL,
                website="http://generalhospital.com",
                operating_hours="Mon-Fri 8:00-20:00, Sat 8:00-14:00"
            ),
            MedicalFacility(
                facility_id=2,
                name="Downtown Clinic",
                address="456 Broad Ave, Cityville",
                phone_number="123-555-0199",
                facility_type=FacilityType.CLINIC,
                website="http://downtownclinic.com",
                operating_hours="Mon-Fri 9:00-17:00"
            ),
            MedicalFacility(
                facility_id=3,
                name="City Labs",
                address="789 Maple St, Cityville",
                phone_number="123-555-1122",
                facility_type=FacilityType.LABORATORY,
                website="http://citylabs.com",
                operating_hours="Mon-Fri 7:00-19:00"
            ),
            MedicalFacility(
                facility_id=4,
                name="Main Street Pharmacy",
                address="101 Elm St, Cityville",
                phone_number="123-555-1212",
                facility_type=FacilityType.PHARMACY,
                website="http://mainstreetpharmacy.com",
                operating_hours="Mon-Sun 8:00-22:00"
            )
        ]
        session.add_all(facilities)

        # Section for N-to-N combination tables
        doctor_facility_associations = [
            DoctorFacilityAssociation(doctor_id=1, facility_id=1),
            DoctorFacilityAssociation(doctor_id=2, facility_id=1),
            DoctorFacilityAssociation(doctor_id=3, facility_id=2),
            DoctorFacilityAssociation(doctor_id=1, facility_id=3),
            DoctorFacilityAssociation(doctor_id=4, facility_id=4),
            DoctorFacilityAssociation(doctor_id=2, facility_id=2),
            DoctorFacilityAssociation(doctor_id=5, facility_id=1),
        ]
        session.add_all(doctor_facility_associations)


    # Section for N-to-N combination tables


    # Commit changes
        session.commit()

        print("Done")

insert_mock_data()