from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import BaseModel
from sqlmodel import Session, select

from models import *
from database import engine, get_db
from security import hash_password, verify_password, create_token, oauth2_scheme, verify_token

auth_router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: str
    password: str


description = """
### Register a New User

Registers a new user in the system.
Upon successful registration, the endpoint returns a **access token**.
The token is valid for 2 hours, after which a new token must be obtained to continue making API calls.

- **Refresh Token Expiration**: 2 hours
- **Usage**: Include the token in the `Authorization` header to authenticate requests.
- **Purpose**: Interact with protected API resources
"""


@auth_router.post("/register/", tags=["auth"], description=description)
def register_user(email: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).where(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    # Hash the password
    hashed_password = hash_password(password)

    # Create a new user
    new_user = User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate a JWT token for the newly registered user
    access_token = create_token(data={"sub": db_user.email, "type": "refresh_token"}, expires_delta=timedelta(hours=2))
    return {"access_token": access_token, "token_type": "bearer"}

description = """
### Obtain Access Token

This endpoint returns both a **access token** upon successful login.
The token is valid for 2 hours, after which a new token must be obtained to continue making API calls.

- **Access Token Expiration**: 2 hours
- **Usage**: Include the token in the `Authorization` header to authenticate requests.
- **Purpose**: Interact with protected API resources
"""

@auth_router.post("/login", tags=['auth'], description=description)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
db: Session = Depends(get_db)):
    db_user = db.query(User).where(User.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    else:
        access_token = create_token(data={"sub": db_user.email, "type": "refresh_token"}, expires_delta=timedelta(hours=2))

        return {"access_token": access_token, "token_type": "bearer"}

    return None


description = """
### API Endpoint: Obtain Access Token

This endpoint issues an access token, required to authenticate and authorize API requests.\
The token is valid for 2 hours, after which a new token must be obtained to continue making API calls.

- **Usage**: Include the token in the `Authorization` header to authenticate requests.
- **Token Lifetime**: 2 hours
- **Purpose**: Interact with protected API resources
"""

@auth_router.get("/get_token", tags=['auth'], description=description)
def get_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = verify_token(token)
        email: str = payload.get("sub")
        type: str = payload.get("type")

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"})

    if type == "refresh_token":
        access_token = create_token(data={"sub": email, "type": "access_token"},
                                     expires_delta=timedelta(hours=2))

        return {"access_token": access_token, "token_type": "bearer"}


description = """
### API Endpoint: Obtain Access Token

This endpoint issues an access token, required to authenticate and authorize API requests.\

- **Usage**: Include the token in the `Authorization` header to authenticate requests.
- **Token Lifetime**: 2 hours
- **Purpose**: Interact with protected API resources
"""

@auth_router.post("/extend_session", tags=['auth'], description=description)
def get_token(token: Annotated[str, Form()]):
    try:
        payload = verify_token(token)
        email: str = payload.get("sub")
        type: str = payload.get("type")

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"})

    if type == "refresh_token":
        access_token = create_token(data={"sub": email, "type": "access_token"},
                                     expires_delta=timedelta(hours=2))

        return {"access_token": access_token, "token_type": "bearer"}