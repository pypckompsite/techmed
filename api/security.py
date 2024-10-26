from typing import Annotated

from fastapi import Depends, HTTPException, Cookie
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import pyotp
from starlette import status

# Use Argon2 for hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto",
                            argon2__time_cost=25,
                            argon2__memory_cost=128 *1024,
                            argon2__parallelism=4,
                            argon2__hash_len=64,
                            argon2__salt_size=16)

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(access_token: Annotated[str | None, Cookie()] = None):
    print(access_token)
    if not access_token:
        print('No token')
        raise credentials_exception
    try:
        # Decode the JWT token
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            print("No email")
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception



def encrypt_field(data: str):
    return data


def decrypt_field(data: str):
    return data