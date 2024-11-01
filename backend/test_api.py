import time

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from api.main import app
from api.insert_mock_data import insert_mock_data
from api.security import public_key, ALGORITHM

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
    assert response.status_code == 201
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
    assert response.status_code == 201
    assert len(client.cookies.get("access_token")) > 0

def test_register_same_email():    #User with same email
    response = client.post("/auth/register",
                           data={"email": "test@techmed.stasiak", "password": "%*Secure*Password12345"})
    assert response.status_code == 201
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
    assert response.status_code == 201
    assert len(client.cookies.get("access_token")) > 0

    response = client.post("/auth/login", data={"email": "test@techmed.stasiak", "password": "%*Secure*Password12345"})
    assert response.status_code == 200
    assert len(client.cookies.get("access_token")) > 0




def test_change_password_valid():
    client.cookies["access_token"] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMUBleGFtcGxlLmNvbSIsInR5cGUiOiJQYXRpZW50IiwiZXhwIjo5OTk5OTk5OTk5fQ.B1_-fEfFvagHKN_zz1gl1r8-fQPLcxqCSNLR790d7-SCVlZAQ8UIkOp65DkOJrbe-EbGnxCdNmUczIK0eNIFgkQwul-eEjwgbUK8z1SOkArYK7vD95BgShb4awfsXqgRPtYVF3YNYfiVCD3PuCAgzWTDuWfs-oiGUrMt4eew6yprsm_AxW0l7LzSuG9xu8GkCkdg_jkoWrOqCRpaN2skltcBF1RhFtUMovH_iGP9pUdaM6bYsrw4rkQxbnJGYSC0fXZ6mWrqxq_58w701gTWBDBwX1RZt2KaLkjfMrB_BW1Z70bXl_I7NY2OCm0HaRnu7LsbNwLkJXpYXnLFvVaJPRAXj_rGzHzMOucIzsij8nyMahF9CI9fut60DZWzdzkoNkydpWyvBdzl7cLfBRrwPlrxVCqByak9Z_nqZDEtziKiNe_BRSYXgDgR4Nixf0v3TntBrgtwRYzIiFgFEcPB3dbH5Uhj4mjmBn3D_gMfi2wQuabu0zVsIUKGIocmC7koij6H5_3_VVnLaIJJxcZmM8OihhnIhTLh0-sMtvSOlzQM8nrXRw_RdETseZqCHX3-m3mbNlD2IGfvWEfeTyoEpu3jJzthWHeJXWnAaJLEX83MDyPHyGL_e3VlUEGWibcN5mQnMFk81th0vo-RoBI6Q74dWRjNdpkXbi20mp4xtf4"

    response = client.post("/auth/change_password", data={"current_password": "password", "new_password": "bardzobezpiecznehaslo"})
    assert response.status_code == 200

    response = client.post("/auth/login", data={"email": "user1@example.com", "password": "bardzobezpiecznehaslo"})
    assert response.status_code == 200

def test_change_password_invalid_current_password():
    client.cookies["access_token"] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMUBleGFtcGxlLmNvbSIsInR5cGUiOiJQYXRpZW50IiwiZXhwIjo5OTk5OTk5OTk5fQ.B1_-fEfFvagHKN_zz1gl1r8-fQPLcxqCSNLR790d7-SCVlZAQ8UIkOp65DkOJrbe-EbGnxCdNmUczIK0eNIFgkQwul-eEjwgbUK8z1SOkArYK7vD95BgShb4awfsXqgRPtYVF3YNYfiVCD3PuCAgzWTDuWfs-oiGUrMt4eew6yprsm_AxW0l7LzSuG9xu8GkCkdg_jkoWrOqCRpaN2skltcBF1RhFtUMovH_iGP9pUdaM6bYsrw4rkQxbnJGYSC0fXZ6mWrqxq_58w701gTWBDBwX1RZt2KaLkjfMrB_BW1Z70bXl_I7NY2OCm0HaRnu7LsbNwLkJXpYXnLFvVaJPRAXj_rGzHzMOucIzsij8nyMahF9CI9fut60DZWzdzkoNkydpWyvBdzl7cLfBRrwPlrxVCqByak9Z_nqZDEtziKiNe_BRSYXgDgR4Nixf0v3TntBrgtwRYzIiFgFEcPB3dbH5Uhj4mjmBn3D_gMfi2wQuabu0zVsIUKGIocmC7koij6H5_3_VVnLaIJJxcZmM8OihhnIhTLh0-sMtvSOlzQM8nrXRw_RdETseZqCHX3-m3mbNlD2IGfvWEfeTyoEpu3jJzthWHeJXWnAaJLEX83MDyPHyGL_e3VlUEGWibcN5mQnMFk81th0vo-RoBI6Q74dWRjNdpkXbi20mp4xtf4"

    response = client.post("/auth/change_password", data={"current_password": "password1", "new_password": "bardzobezpiecznehaslo"})
    assert response.status_code == 401

def test_change_password_invalid_new_password():
    client.cookies["access_token"] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMUBleGFtcGxlLmNvbSIsInR5cGUiOiJQYXRpZW50IiwiZXhwIjo5OTk5OTk5OTk5fQ.B1_-fEfFvagHKN_zz1gl1r8-fQPLcxqCSNLR790d7-SCVlZAQ8UIkOp65DkOJrbe-EbGnxCdNmUczIK0eNIFgkQwul-eEjwgbUK8z1SOkArYK7vD95BgShb4awfsXqgRPtYVF3YNYfiVCD3PuCAgzWTDuWfs-oiGUrMt4eew6yprsm_AxW0l7LzSuG9xu8GkCkdg_jkoWrOqCRpaN2skltcBF1RhFtUMovH_iGP9pUdaM6bYsrw4rkQxbnJGYSC0fXZ6mWrqxq_58w701gTWBDBwX1RZt2KaLkjfMrB_BW1Z70bXl_I7NY2OCm0HaRnu7LsbNwLkJXpYXnLFvVaJPRAXj_rGzHzMOucIzsij8nyMahF9CI9fut60DZWzdzkoNkydpWyvBdzl7cLfBRrwPlrxVCqByak9Z_nqZDEtziKiNe_BRSYXgDgR4Nixf0v3TntBrgtwRYzIiFgFEcPB3dbH5Uhj4mjmBn3D_gMfi2wQuabu0zVsIUKGIocmC7koij6H5_3_VVnLaIJJxcZmM8OihhnIhTLh0-sMtvSOlzQM8nrXRw_RdETseZqCHX3-m3mbNlD2IGfvWEfeTyoEpu3jJzthWHeJXWnAaJLEX83MDyPHyGL_e3VlUEGWibcN5mQnMFk81th0vo-RoBI6Q74dWRjNdpkXbi20mp4xtf4"

    response = client.post("/auth/change_password", data={"current_password": "password", "new_password": "qwerty"})
    assert response.status_code == 400


def test_verify_token_valid():
    client.cookies["access_token"] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMUBleGFtcGxlLmNvbSIsInR5cGUiOiJQYXRpZW50IiwiZXhwIjo5OTk5OTk5OTk5fQ.B1_-fEfFvagHKN_zz1gl1r8-fQPLcxqCSNLR790d7-SCVlZAQ8UIkOp65DkOJrbe-EbGnxCdNmUczIK0eNIFgkQwul-eEjwgbUK8z1SOkArYK7vD95BgShb4awfsXqgRPtYVF3YNYfiVCD3PuCAgzWTDuWfs-oiGUrMt4eew6yprsm_AxW0l7LzSuG9xu8GkCkdg_jkoWrOqCRpaN2skltcBF1RhFtUMovH_iGP9pUdaM6bYsrw4rkQxbnJGYSC0fXZ6mWrqxq_58w701gTWBDBwX1RZt2KaLkjfMrB_BW1Z70bXl_I7NY2OCm0HaRnu7LsbNwLkJXpYXnLFvVaJPRAXj_rGzHzMOucIzsij8nyMahF9CI9fut60DZWzdzkoNkydpWyvBdzl7cLfBRrwPlrxVCqByak9Z_nqZDEtziKiNe_BRSYXgDgR4Nixf0v3TntBrgtwRYzIiFgFEcPB3dbH5Uhj4mjmBn3D_gMfi2wQuabu0zVsIUKGIocmC7koij6H5_3_VVnLaIJJxcZmM8OihhnIhTLh0-sMtvSOlzQM8nrXRw_RdETseZqCHX3-m3mbNlD2IGfvWEfeTyoEpu3jJzthWHeJXWnAaJLEX83MDyPHyGL_e3VlUEGWibcN5mQnMFk81th0vo-RoBI6Q74dWRjNdpkXbi20mp4xtf4"


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
    payload = jwt.decode(response.cookies['access_token'], public_key, algorithms=[ALGORITHM])
    exp_pre = payload['exp']

    time.sleep(2)

    response = client.get("/auth/extend_session")
    assert response.status_code == 200
    payload = jwt.decode(response.cookies['access_token'], public_key, algorithms=[ALGORITHM])
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
    client.cookies["access_token"] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInR5cGUiOiJQYXRpZW50IiwiZXhwIjo5OTk5OTk5OTk5fQ.fLWLnCzWqpDmoGS4Wb3X37YAPC9y1pUUF25KjVHKJh3Rxpq3M0qIbNQai80_STG-A7UhrHuAIh51bx9F2jgkG8xGiCSNCuaMN86cHDHn6UPvj6OjExmbiBHWlRzAnNNp76oheBDhajFuZklHwL7WqvYTLoAv9TXwy5hr0VEhnKcJe9TBueKjhYZpz9EgKb6_UJ1u5Psny2YkIinwdG9E8jq8PNHQRf25CNf70CtYDzDYadj60eb_KaCWFS07qTxjH6GWwGgDgC-dQ-nkkEYfiAytp3gbzhcJnbJ28NC6dOGbonPHM-mlxoAzuIBL_BVnb-SMOnMZqVSogRh0WfJZ-_SYDnrBblQirINY3Zlp2xHZGBYtqwGz1R1VSPIcJjRCEJl3ipzkWICx7sbybt1uL3b7tCWQQdToehHhkWCqjlWq75jf6GhAZPkzKrTzXiD_bdw9iIu0rPRJ_741CxO_RYpbuySGPkmfASiUpgOyMSlGrhg-nfZcZ-Rh6f90LoDozfQJXo4q2EOHPCF9Zkveb-UI4jlqCE1xB4J3hrza9iWXum0FuT54zLcyu-AgfrzvouA1x9kp08VkHCfw_whwQzvjMlzB5KFpA5zWxEm42R2ZCzsgZaXvD2P5mD5kzH15MRj_BcJsM2BQpIOXmd1yjHs76OD2tnSUcSr1qmPFX2o"

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

    assert response.status_code == 201
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
    client.cookies["access_token"] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInR5cGUiOiJQYXRpZW50IiwiZXhwIjo5OTk5OTk5OTk5fQ.fLWLnCzWqpDmoGS4Wb3X37YAPC9y1pUUF25KjVHKJh3Rxpq3M0qIbNQai80_STG-A7UhrHuAIh51bx9F2jgkG8xGiCSNCuaMN86cHDHn6UPvj6OjExmbiBHWlRzAnNNp76oheBDhajFuZklHwL7WqvYTLoAv9TXwy5hr0VEhnKcJe9TBueKjhYZpz9EgKb6_UJ1u5Psny2YkIinwdG9E8jq8PNHQRf25CNf70CtYDzDYadj60eb_KaCWFS07qTxjH6GWwGgDgC-dQ-nkkEYfiAytp3gbzhcJnbJ28NC6dOGbonPHM-mlxoAzuIBL_BVnb-SMOnMZqVSogRh0WfJZ-_SYDnrBblQirINY3Zlp2xHZGBYtqwGz1R1VSPIcJjRCEJl3ipzkWICx7sbybt1uL3b7tCWQQdToehHhkWCqjlWq75jf6GhAZPkzKrTzXiD_bdw9iIu0rPRJ_741CxO_RYpbuySGPkmfASiUpgOyMSlGrhg-nfZcZ-Rh6f90LoDozfQJXo4q2EOHPCF9Zkveb-UI4jlqCE1xB4J3hrza9iWXum0FuT54zLcyu-AgfrzvouA1x9kp08VkHCfw_whwQzvjMlzB5KFpA5zWxEm42R2ZCzsgZaXvD2P5mD5kzH15MRj_BcJsM2BQpIOXmd1yjHs76OD2tnSUcSr1qmPFX2o"

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
        "middle_name": "Adam",
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
        "middle_name": "Adam",
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
        "middle_name": "Adam",
        "last_name": "Doe",
        "PESEL": "62042",
        "gender": "M",
        "address": "123 Main St, City, Country",
        "phone_number": "123456789"
    }

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 422

    # Invalid gender
    patient_data = {
        "email": "test@example.com",
        "first_name": "John",
        "middle_name": "Adam",
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
        "middle_name": "Adam",
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
    client.cookies["access_token"] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInR5cGUiOiJQYXRpZW50IiwiZXhwIjo5OTk5OTk5OTk5fQ.fLWLnCzWqpDmoGS4Wb3X37YAPC9y1pUUF25KjVHKJh3Rxpq3M0qIbNQai80_STG-A7UhrHuAIh51bx9F2jgkG8xGiCSNCuaMN86cHDHn6UPvj6OjExmbiBHWlRzAnNNp76oheBDhajFuZklHwL7WqvYTLoAv9TXwy5hr0VEhnKcJe9TBueKjhYZpz9EgKb6_UJ1u5Psny2YkIinwdG9E8jq8PNHQRf25CNf70CtYDzDYadj60eb_KaCWFS07qTxjH6GWwGgDgC-dQ-nkkEYfiAytp3gbzhcJnbJ28NC6dOGbonPHM-mlxoAzuIBL_BVnb-SMOnMZqVSogRh0WfJZ-_SYDnrBblQirINY3Zlp2xHZGBYtqwGz1R1VSPIcJjRCEJl3ipzkWICx7sbybt1uL3b7tCWQQdToehHhkWCqjlWq75jf6GhAZPkzKrTzXiD_bdw9iIu0rPRJ_741CxO_RYpbuySGPkmfASiUpgOyMSlGrhg-nfZcZ-Rh6f90LoDozfQJXo4q2EOHPCF9Zkveb-UI4jlqCE1xB4J3hrza9iWXum0FuT54zLcyu-AgfrzvouA1x9kp08VkHCfw_whwQzvjMlzB5KFpA5zWxEm42R2ZCzsgZaXvD2P5mD5kzH15MRj_BcJsM2BQpIOXmd1yjHs76OD2tnSUcSr1qmPFX2o"

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

    assert response.status_code == 201

    response = client.post("/admin/patients/add", json=patient_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"


def test_list_users_admin():
    client.cookies["access_token"] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInR5cGUiOiJQYXRpZW50IiwiZXhwIjo5OTk5OTk5OTk5fQ.fLWLnCzWqpDmoGS4Wb3X37YAPC9y1pUUF25KjVHKJh3Rxpq3M0qIbNQai80_STG-A7UhrHuAIh51bx9F2jgkG8xGiCSNCuaMN86cHDHn6UPvj6OjExmbiBHWlRzAnNNp76oheBDhajFuZklHwL7WqvYTLoAv9TXwy5hr0VEhnKcJe9TBueKjhYZpz9EgKb6_UJ1u5Psny2YkIinwdG9E8jq8PNHQRf25CNf70CtYDzDYadj60eb_KaCWFS07qTxjH6GWwGgDgC-dQ-nkkEYfiAytp3gbzhcJnbJ28NC6dOGbonPHM-mlxoAzuIBL_BVnb-SMOnMZqVSogRh0WfJZ-_SYDnrBblQirINY3Zlp2xHZGBYtqwGz1R1VSPIcJjRCEJl3ipzkWICx7sbybt1uL3b7tCWQQdToehHhkWCqjlWq75jf6GhAZPkzKrTzXiD_bdw9iIu0rPRJ_741CxO_RYpbuySGPkmfASiUpgOyMSlGrhg-nfZcZ-Rh6f90LoDozfQJXo4q2EOHPCF9Zkveb-UI4jlqCE1xB4J3hrza9iWXum0FuT54zLcyu-AgfrzvouA1x9kp08VkHCfw_whwQzvjMlzB5KFpA5zWxEm42R2ZCzsgZaXvD2P5mD5kzH15MRj_BcJsM2BQpIOXmd1yjHs76OD2tnSUcSr1qmPFX2o"

    response = client.get("/admin/users")
    assert response.status_code == 200
    assert response.json()[0] == { "id": 1,   "email": "user0@example.com",  "mfa_type": None, "type": "Patient" }



def test_get_user_data_admin():
    client.cookies["access_token"] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInR5cGUiOiJQYXRpZW50IiwiZXhwIjo5OTk5OTk5OTk5fQ.fLWLnCzWqpDmoGS4Wb3X37YAPC9y1pUUF25KjVHKJh3Rxpq3M0qIbNQai80_STG-A7UhrHuAIh51bx9F2jgkG8xGiCSNCuaMN86cHDHn6UPvj6OjExmbiBHWlRzAnNNp76oheBDhajFuZklHwL7WqvYTLoAv9TXwy5hr0VEhnKcJe9TBueKjhYZpz9EgKb6_UJ1u5Psny2YkIinwdG9E8jq8PNHQRf25CNf70CtYDzDYadj60eb_KaCWFS07qTxjH6GWwGgDgC-dQ-nkkEYfiAytp3gbzhcJnbJ28NC6dOGbonPHM-mlxoAzuIBL_BVnb-SMOnMZqVSogRh0WfJZ-_SYDnrBblQirINY3Zlp2xHZGBYtqwGz1R1VSPIcJjRCEJl3ipzkWICx7sbybt1uL3b7tCWQQdToehHhkWCqjlWq75jf6GhAZPkzKrTzXiD_bdw9iIu0rPRJ_741CxO_RYpbuySGPkmfASiUpgOyMSlGrhg-nfZcZ-Rh6f90LoDozfQJXo4q2EOHPCF9Zkveb-UI4jlqCE1xB4J3hrza9iWXum0FuT54zLcyu-AgfrzvouA1x9kp08VkHCfw_whwQzvjMlzB5KFpA5zWxEm42R2ZCzsgZaXvD2P5mD5kzH15MRj_BcJsM2BQpIOXmd1yjHs76OD2tnSUcSr1qmPFX2o"

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



