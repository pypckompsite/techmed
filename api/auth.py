import re
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Form, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import BaseModel, EmailStr, validator, field_validator
from sqlmodel import Session, select
from starlette import status


from security import credentials_exception
from functions import *
from models import *
from database import get_db
from security import hash_password, verify_password, create_token, verify_token
auth_router = APIRouter()
email_regex = r"^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$"
email_pattern = re.compile(email_regex, re.IGNORECASE)


with open("wordlist_pl.txt", 'r') as file:
    weak_passwords_set = {line.strip() for line in file if line.strip()}


def validate_email(email: str) -> bool:
    return bool(email_pattern.fullmatch(email))

# Define the Pydantic model with validation
class UserRegistration(BaseModel):
    email: str
    password: str

    @field_validator("email")
    def validate_email(cls, value):

        if not validate_email(value):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email address")
        return value
    # Password complexity validator
    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 12:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The password must be at least 12 characters long.")
        if value in weak_passwords_set:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This password is considered too weak")
        return value


class ChangePassword(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    def validate_password(cls, value):
        if len(value) < 12:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The password must be at least 12 characters long.")
        if value in weak_passwords_set:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This password is considered too weak")
        return value


@auth_router.post("/register/", tags=["auth"])
def register_user(response: Response, email: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):
    """
    ### Register a New User

    Registers a new user in the system.
    Upon successful registration, the endpoint returns a **access token**.
    The token is valid for 2 hours, after which a new token must be obtained to continue making API calls.
    """

    user_data = UserRegistration(email=email, password=password)

    # Check if user already exists
    stmt = select(User).where(User.email == user_data.email)
    db_user = db.exec(stmt).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create a new user
    new_user = User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate a JWT token for the newly registered user
    access_token = create_token(data={"sub": new_user.email},
                               expires_delta=timedelta(hours=2))

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=2 * 3600,  # Expires in 30 minutes
        secure=False,  # Set this to True in production to only send over HTTPS
    )
    return {"message": "Register successful"}

@auth_router.post("/login", tags=['auth'])
def login(response: Response,
          email: Annotated[str, Form()],
          password: Annotated[str, Form()],
          db: Session = Depends(get_db)):
    """
    ### Obtain Access Token

    This endpoint returns both a **access token** upon successful login.
    The token is valid for 2 hours, after which a new token must be obtained to continue making API calls.
    """
    stmt = select(User).where(User.email == email)
    db_user = db.exec(stmt).first()
    if not db_user:
        hash_password(password)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    elif not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    else:
        access_token = create_token(data={"sub": db_user.email},
                                    expires_delta=timedelta(hours=2))
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=3 * 3600,  # Expires in 30 minutes
            secure=False,  # Set this to True in production to only send over HTTPS
        )
        return {"message": "Login successful"}



@auth_router.post("/change_password", summary="Change User Password", tags=["auth"])
async def change_user_password(
        current_password: Annotated[str, Form()],
        new_password: Annotated[str, Form()],
        payload: dict = Depends(verify_token),
        db: Session = Depends(get_db)):
    """
    Endpoint to change the user's password.

    This endpoint requires the user to provide their current password for verification.
    If verified, the password will be updated to the new password provided.

    - **current_password**: The user's current password (required).
    - **new_password**: The new password the user wants to set (required).
    """
    email = payload["sub"]

    data = ChangePassword(current_password=current_password, new_password=new_password)

    stmt = select(User).where(User.email == email)
    user = db.exec(stmt).first()

    if not verify_password(data.current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )

    user.hashed_password = hash_password(data.new_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Password change successful"}


@auth_router.get("/extend_session", tags=['auth'])
def extend_session(response: Response, payload: dict = Depends(verify_token)):
    """
    ### API Endpoint: Extend Access Token

    This endpoint issues an access token, required to authenticate and authorize API requests.\
    The token is valid for 2 hours, after which a new token must be obtained to continue making API calls.
    """

    email: str = payload.get("sub")


    access_token = create_token(data={"sub": email},
                                expires_delta=timedelta(hours=2))

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=2 * 3600,  # Expires in 30 minutes
        secure=False,  # Set this to True in production to only send over HTTPS
    )
    return {"message": "Session extend successful"}


@auth_router.get("/verify_token", tags=['auth'])
def extend_session(db: Session = Depends(get_db), payload: dict = Depends(verify_token)):
    """
    ### API Endpoint: Verify Access Token

    This endpoint allows you to obtain information about the user's access token.'
    """
    email: str = payload.get("sub")

    stmt = select(User).where(User.email == email)
    user = db.exec(stmt).first()
    if not user:
        raise credentials_exception

    return {"email": user.email, "type": user.type.name}


@auth_router.get("/get-my-info", tags=['auth'])
def get_info(payload: dict = Depends(get_my_info)):
   return payload