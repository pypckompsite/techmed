import time

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from backend.api.main import app
from api.insert_mock_data import insert_mock_data

from api.security import SECRET_KEY, ALGORITHM

client = TestClient(app, base_url="https://localhost:8000")

@pytest.fixture(autouse=True)
def reset_state():
    global client
    insert_mock_data()
    client = TestClient(app)

def test_login_auth_valid():
    response = client.post("/auth/login", data={"email": "user1@example.com", "password": "password"})
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0

def test_login_auth_invalid_login():
    response = client.post("/auth/login", data={"email": "none@example.com", "password": "password"})
    assert response.status_code == 401

def test_login_auth_invalidpassword():
    response = client.post("/auth/login", data={"email": "user1@example.com", "password": "qwerty"})
    assert response.status_code == 401





def test_register_auth_valid():
    response = client.post("/auth/register", data={"email": "test@techmed.stasiak", "password": "%*Secure*Password12345"})
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0

def test_register_auth_valid_longpassword():
    password = """Litwo! Ojczyzno moja! ty jesteś jak zdrowie:
Ile cię trzeba cenić, ten tylko się dowie,
Kto cię stracił. Dziś piękność twą w całej ozdobie
Widzę i opisuję, bo tęsknię po tobie.

    Panno święta, co Jasnej bronisz Częstochowy
I w Ostrej świecisz Bramie! Ty, co gród zamkowy
Nowogródzki ochraniasz z jego wiernym ludem!
Jak mnie dziecko do zdrowia powróciłaś cudem
(Gdy od płaczącej matki, pod Twoją opiekę
Ofiarowany, martwą podniosłem powiekę;
I zaraz mogłem pieszo, do Twych świątyń progu
Iść za wrócone życie podziękować Bogu),
Tak nas powrócisz cudem na Ojczyzny łono.
Tymczasem przenoś moją duszę utęsknioną
Do tych pagórków leśnych, do tych łąk zielonych,
Szeroko nad błękitnym Niemnem rozciągnionych;
Do tych pól malowanych zbożem rozmaitem,
Wyzłacanych pszenicą, posrebrzanych żytem;
Gdzie bursztynowy świerzop, gryka jak śnieg biała,
Gdzie panieńskim rumieńcem dzięcielina pała,
A wszystko przepasane jakby wstęgą, miedzą
Zieloną, na niej z rzadka ciche grusze siedzą."""


    response = client.post("/auth/register", data={"email": "test@techmed.stasiak", "password": password})
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0

def test_register_same_email():    #User with same email
    response = client.post("/auth/register",
                           data={"email": "test@techmed.stasiak", "password": "%*Secure*Password12345"})
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0

    response = client.post("/auth/register", data={"email": "test@techmed.stasiak", "password": "%*Secure*Password12345"})
    assert response.status_code == 400
    assert len(client.cookies.get("access_token")) > 0

def test_register_invalid_email():
    response = client.post("/auth/register", data={"email": "test", "password": "%*Secure*Password12345"})
    assert response.status_code == 400

def test_register_invalid_password():
    response = client.post("/auth/register", data={"email": "test@techmed.stasiak", "password": "pass"})
    assert response.status_code == 400

def test_register_weak_password():
    response = client.post("/auth/register", data={"email": "test@techmed.stasiak", "password": "123hfjdk147"})
    assert response.status_code == 400



def test_register_login_auth_valid():
    response = client.post("/auth/register", data={"email": "test@techmed.stasiak", "password": "%*Secure*Password12345"})
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0

    response = client.post("/auth/login", data={"email": "test@techmed.stasiak", "password": "%*Secure*Password12345"})
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0




def test_change_password_valid():
    client.cookies["access_token"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6OTk5OTk5OTk5OX0.KnOTiQ_gBUAu35bfyDUZoPUjJAiZJZ7J0ts0KbPW9F4"

    response = client.post("/auth/change_password", data={"current_password": "password", "new_password": "bardzobezpiecznehaslo"})
    assert response.status_code == 200

    response = client.post("/auth/login", data={"email": "user1@example.com", "password": "bardzobezpiecznehaslo"})
    assert response.status_code == 200

def test_change_password_invalid_current_password():
    client.cookies["access_token"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6OTk5OTk5OTk5OX0.KnOTiQ_gBUAu35bfyDUZoPUjJAiZJZ7J0ts0KbPW9F4"

    response = client.post("/auth/change_password", data={"current_password": "password1", "new_password": "bardzobezpiecznehaslo"})
    assert response.status_code == 401

def test_change_password_invalid_new_password():
    client.cookies["access_token"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6OTk5OTk5OTk5OX0.KnOTiQ_gBUAu35bfyDUZoPUjJAiZJZ7J0ts0KbPW9F4"

    response = client.post("/auth/change_password", data={"current_password": "password", "new_password": "qwerty"})
    assert response.status_code == 400


def test_verify_token_valid():
    client.cookies["access_token"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6OTk5OTk5OTk5OX0.KnOTiQ_gBUAu35bfyDUZoPUjJAiZJZ7J0ts0KbPW9F4"


    response = client.get("/auth/verify_token")
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0


def test_verify_token_no_token():

    response = client.get("/auth/verify_token")
    assert response.status_code == 401

def test_verify_token_invalid_token():
    client.cookies["access_token"] = "invalid"

    response = client.get("/auth/verify_token")
    assert response.status_code == 401

def test_extend_session_valid():
    response = client.post("/auth/login", data={"email": "user1@example.com", "password": "password"})
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0
    payload = jwt.decode(response.cookies['access_token'], SECRET_KEY, algorithms=[ALGORITHM])
    exp_pre = payload['exp']

    time.sleep(2)

    response = client.get("/auth/extend_session")
    assert response.status_code == 200
    payload = jwt.decode(response.cookies['access_token'], SECRET_KEY, algorithms=[ALGORITHM])
    exp_post = payload['exp']
    assert exp_post > exp_pre

def test_extend_session_no_token():
    response = client.get("/auth/extend_session")
    assert response.status_code == 401

def test_extend_session_invalid_token():
    client.cookies["access_token"] = "invalid"

    response = client.get("/auth/extend_session")
    assert response.status_code == 401


def test_admin_create_patient():
    client.cookies["access_token"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsImV4cCI6OTk5OTk5OTk5OX0.ZYSHAhu60Yilq95rohK2cMMOPgR1O_3ucbKFWPU3luo"

    patient_data = {
        "email": "test@example.com",
        "first_name": "John",
        "middle_name": "Adam",
        "last_name": "Doe",
        "PESEL": "62042621665",
        "gender": "M",
        "address": "123 Main St, City, Country",
        "phone_number": "123456789"
    }

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 200
    assert response.json()["message"] == "Patient created"
    assert (response.json()["patient_temp_password"]
            and response.json()["patient_temp_password"] is not None
            and len(response.json()["patient_temp_password"]) > 12)

def test_admin_create_patient_no_token():

    patient_data = {
        "email": "test@example.com",
        "first_name": "John",
        "middle_name": "Adam",
        "last_name": "Doe",
        "PESEL": "62042621665",
        "gender": "M",
        "address": "123 Main St, City, Country",
        "phone_number": "123456789"
    }

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 401


def test_admin_create_patient_invalid_data():
    client.cookies["access_token"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsImV4cCI6OTk5OTk5OTk5OX0.ZYSHAhu60Yilq95rohK2cMMOPgR1O_3ucbKFWPU3luo"

    # Invalid email address
    patient_data = {
        "email": "testtest",
        "first_name": "John",
        "middle_name": "Adam",
        "last_name": "Doe",
        "PESEL": "62042621665",
        "gender": "M",
        "address": "123 Main St, City, Country",
        "phone_number": "123456789"
    }

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email address must be valid"

    # Invalid first name
    patient_data = {
        "email": "test@example.com",
        "first_name": "John!!!",
        "middle_name": "Adam",
        "last_name": "Doe",
        "PESEL": "62042621665",
        "gender": "M",
        "address": "123 Main St, City, Country",
        "phone_number": "123456789"
    }

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "First name must contain only letters"

    # Invalid middle name
    patient_data = {
        "email": "test@example.com",
        "first_name": "John",
        "middle_name": "A.%%5",
        "last_name": "Doe",
        "PESEL": "62042621665",
        "gender": "M",
        "address": "123 Main St, City, Country",
        "phone_number": "123456789"
    }

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Middle name must contain only letters"

    # Invalid last name
    patient_data = {
        "email": "test@example.com",
        "first_name": "John",
        "middle_name": "Adam",
        "last_name": "69Doe",
        "PESEL": "62042621665",
        "gender": "M",
        "address": "123 Main St, City, Country",
        "phone_number": "123456789"
    }

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Last name must contain only letters"

    # Invalid pesel1
    patient_data = {
        "email": "test@example.com",
        "first_name": "John",
        "middle_name": "A.",
        "last_name": "Doe",
        "PESEL": "6204262186E",
        "gender": "M",
        "address": "123 Main St, City, Country",
        "phone_number": "123456789"
    }

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "PESEL must contain only digits."

    # Invalid pesel2
    patient_data = {
        "email": "test@example.com",
        "first_name": "John",
        "middle_name": "A.",
        "last_name": "Doe",
        "PESEL": "62042621667",
        "gender": "M",
        "address": "123 Main St, City, Country",
        "phone_number": "123456789"
    }

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid PESEL: checksum does not match."

    # Invalid pesel3
    patient_data = {
        "email": "test@example.com",
        "first_name": "John",
        "middle_name": "A.",
        "last_name": "Doe",
        "PESEL": "62042",
        "gender": "M",
        "address": "123 Main St, City, Country",
        "phone_number": "123456789"
    }

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "PESEL must be exactly 11 digits long."

    # Invalid gender
    patient_data = {
        "email": "test@example.com",
        "first_name": "John",
        "middle_name": "A.",
        "last_name": "Doe",
        "PESEL": "12345678901",
        "gender": "X",
        "address": "123 Main St, City, Country",
        "phone_number": "123456789"
    }

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Gender is invalid"

    # Invalid phone number
    patient_data = {
        "email": "test@example.com",
        "first_name": "John",
        "middle_name": "A.",
        "last_name": "Doe",
        "PESEL": "12345678901",
        "gender": "M",
        "address": "123 Main St, City, Country",
        "phone_number": "5678"
    }

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Phone number must valid"

    # Invalid address
    patient_data = {
        "email": "test@example.com",
        "first_name": "John",
        "middle_name": "Adam",
        "last_name": "Doe",
        "PESEL": "62042621665",
        "gender": "M",
        "address": "%%%%%%%%%<",
        "phone_number": "123456789"
    }

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Address contains invalid characters."

def test_admin_create_patient_already_exists():
    client.cookies[
        "access_token"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsImV4cCI6OTk5OTk5OTk5OX0.ZYSHAhu60Yilq95rohK2cMMOPgR1O_3ucbKFWPU3luo"

    # Invalid email address
    patient_data = {
        "email": "test@example.com",
        "first_name": "John",
        "middle_name": "Adam",
        "last_name": "Doe",
        "PESEL": "62042621665",
        "gender": "M",
        "address": "123 Main St, City, Country",
        "phone_number": "123456789"
    }

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 200

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"


def test_list_users_admin():
    client.cookies["access_token"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsImV4cCI6OTk5OTk5OTk5OX0.ZYSHAhu60Yilq95rohK2cMMOPgR1O_3ucbKFWPU3luo"

    response = client.get("/admin/users")
    assert response.status_code == 200
    assert response.json()[0] == { "id": 1,   "email": "user0@example.com",  "mfa_type": None, "type": "Patient" }



def test_get_user_data_admin():
    client.cookies[
        "access_token"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsImV4cCI6OTk5OTk5OTk5OX0.ZYSHAhu60Yilq95rohK2cMMOPgR1O_3ucbKFWPU3luo"

    response = client.get("/admin/users/3")
    assert response.status_code == 200
    assert response.json() == {
                                  "email": "user2@example.com",
                                  "type": "Patient",
                                  "Patient": {
                                    "id": 1,
                                    "last_name": "PatientLastName0",
                                    "gender": "M",
                                    "phone_number": "1234567890",
                                    "first_name": "PatientFirstName0",
                                    "middle_name": "PatientMiddleName0",
                                    "PESEL": "00000000000",
                                    "address": "0 Main St, City, Country"
                                  }
                                }



