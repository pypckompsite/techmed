from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Session, select

from security import verify_token
from models import *
from database import engine, get_db
from security import oauth2_scheme

admin_router = APIRouter()


@admin_router.get("/protected-route")
def protected_route(token: Annotated[str, Depends(oauth2_scheme)]):
    return verify_token(token).get("sub")

#
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#
# class UserCreate(BaseModel):
#     email: str
#     password: str
#
# @auth_router.post("/register/", tags=["auth"], description="Register a new user in the system")
# def register_user(email: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):
#     # Check if user already exists
#     db_user = db.query(User).where(User.email == email).first()
#     if db_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
#
#     # Hash the password
#     hashed_password = hash_password(password)
#
#     # Create a new user
#     new_user = User(email=email, hashed_password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#
#     # Generate a JWT token for the newly registered user
#     access_token = create_access_token(data={"sub": new_user.email})
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
#
# @auth_router.post("/login", tags=['auth'], description="Allows you to obtain login token")
# def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# db: Session = Depends(get_db)):
#     db_user = db.query(User).where(User.email == form_data.username).first()
#     if not db_user or not verify_password(form_data.password, db_user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
#     else:
#         access_token = create_access_token(data={"sub": db_user.email})
#         return {"access_token": access_token, "token_type": "bearer"}
#
#     return None