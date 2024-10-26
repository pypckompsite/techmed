import time

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from main import app
from insert_mock_data import insert_mock_data

from security import SECRET_KEY, ALGORITHM

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
    response = client.post("/auth/login", data={"email": "user1@example.com", "password": "password"})
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0

    response = client.post("/auth/change_password", data={"current_password": "password", "new_password": "bardzobezpiecznehaslo"})
    assert response.status_code == 200

    response = client.post("/auth/login", data={"email": "user1@example.com", "password": "bardzobezpiecznehaslo"})
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0

def test_change_password_invalid_current_password():
    response = client.post("/auth/login", data={"email": "user1@example.com", "password": "password"})
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0

    response = client.post("/auth/change_password", data={"current_password": "password1", "new_password": "bardzobezpiecznehaslo"})
    assert response.status_code == 401

def test_change_password_invalid_new_password():
    response = client.post("/auth/login", data={"email": "user1@example.com", "password": "password"})
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0

    response = client.post("/auth/change_password", data={"current_password": "password", "new_password": "qwerty"})
    assert response.status_code == 400


def test_verify_token_valid():
    response = client.post("/auth/login", data={"email": "user1@example.com", "password": "password"})
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0


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


def test_admin_create_patient():
    response = client.post("/auth/login", data={"email": "admin@example.com", "password": "password"})
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0

    patient_data = {
        "email": "test@example.com",
        "first_name": "John",
        "middle_name": "A.",
        "last_name": "Doe",
        "PESEL": "12345678901",
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