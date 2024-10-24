from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Session, select

from models import *
from database import engine, get_db
from security import hash_password, verify_password, create_access_token, generate_otp_secret, verify_otp

auth_router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str

@auth_router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
db: Session = Depends(get_db)):
    db_user = db.query(User).where(User.email == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not db_user or not verify_password(User.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return None