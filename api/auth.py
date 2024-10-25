from datetime import timedelta
from tkinter.scrolledtext import example
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form, Response, Cookie
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



@auth_router.post("/register/", tags=["auth"])
def register_user(response: Response, email: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):
    """
    ### Register a New User

    Registers a new user in the system.
    Upon successful registration, the endpoint returns a **access token**.
    The token is valid for 2 hours, after which a new token must be obtained to continue making API calls.

    - **Refresh Token Expiration**: 2 hours
    - **Usage**: Include the token in the `Authorization` header to authenticate requests.
    - **Purpose**: Interact with protected API resources
    """
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
    access_token = create_token(data={"sub": new_user.email},
                               expires_delta=timedelta(hours=2))

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800,  # Expires in 30 minutes
        secure=True,  # Set this to True in production to only send over HTTPS
    )
    return {"message": "Register successful"}

@auth_router.post("/login", tags=['auth'])
def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
db: Session = Depends(get_db)):
    """
    ### Obtain Access Token

    This endpoint returns both a **access token** upon successful login.
    The token is valid for 2 hours, after which a new token must be obtained to continue making API calls.

    - **Access Token Expiration**: 2 hours
    - **Usage**: Include the token in the `Authorization` header to authenticate requests.
    - **Purpose**: Interact with protected API resources
    """
    db_user = db.query(User).where(User.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    else:
        access_token = create_token(data={"sub": db_user.email},
                                    expires_delta=timedelta(hours=2))
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=1800,  # Expires in 30 minutes
            secure=True,  # Set this to True in production to only send over HTTPS
        )
        return {"message": "Login successful"}

    return None



@auth_router.post("/change-password", summary="Change User Password", tags=["auth"])
async def change_user_password(
        current_password: Annotated[str, Form()],
        new_password: Annotated[str, Form()],
        access_token: Annotated[str | None, Cookie()] = None,
        db: Session = Depends(get_db)):
    """
    Endpoint to change the user's password.

    This endpoint requires the user to provide their current password for verification.
    If verified, the password will be updated to the new password provided.

    - **current_password**: The user's current password (required).
    - **new_password**: The new password the user wants to set (required).
    """
    payload = verify_token(access_token)
    email = payload["sub"]

    stmt = select(User).where(User.email == email)
    user = db.exec(stmt).first()

    if not verify_password(current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )

    user.hashed_password = hash_password(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return "Password changed successfully"


@auth_router.get("/extend_session", tags=['auth'])
def extend_session(response: Response, access_token: Annotated[str | None, Cookie()] = None):
    """
    ### API Endpoint: Extend Access Token

    This endpoint issues an access token, required to authenticate and authorize API requests.\
    The token is valid for 2 hours, after which a new token must be obtained to continue making API calls.

    - **Usage**: Include the token in the `Authorization` header to authenticate requests.
    - **Token Lifetime**: 2 hours
    - **Purpose**: Interact with protected API resources
    """
    try:
        payload = verify_token(access_token)
        email: str = payload.get("sub")

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"})

    access_token = create_token(data={"sub": email},
                                expires_delta=timedelta(hours=2))

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800,  # Expires in 30 minutes
        secure=True,  # Set this to True in production to only send over HTTPS
    )
    return {"message": "Session extend successful"}


@auth_router.get("/verify_token", tags=['auth'])
def extend_session(response: Response, access_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    """
    ### API Endpoint: Verify Access Token

    This endpoint allows you to obtain information about the user's access token.'

    This returns following JSON:

    {
        "email": "user@example.com",
        "type": "patient"
    }
    """
    try:
        payload = verify_token(access_token)
        email: str = payload.get("sub")

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"})

    user = db.query(User).where(User.email == email).first()
    if not user:
        raise HTTPException(HTTPException(status_code=status.HTTP_401_UNAUTHORIZED))
    type = db.query(UserType).where(UserType.id == user.type).first()
    if not type:
        return {"email": user.email, "type": "N/A"}

    return {"email": user.email, "type": type.name}