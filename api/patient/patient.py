from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Session, select, func

from api.security import generate_secure_password, hash_password
from api.functions import *
from api.models import *
from api.database import engine, get_db
from api.security import credentials_exception


patient_router = APIRouter()

# To be developed further, functionality could be split into multiple files in this new directory. Like CRUD separate from more complicated actions.
# To use this router in more files just import it, and use as usual.