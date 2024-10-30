from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.functions import *
from api.models import *
from api.database import get_db
from api.security import credentials_exception


doctor_router = APIRouter()

# To be developed further, functionality could be split into multiple files in this new directory. Like CRUD separate from more complicated actions.
# To use this router in more files just import it, and use as usual.


@doctor_router.get("/get_my_appointments", tags=["doctor"])
def get_my_appointments(db: Session = Depends(get_db), payload: dict = Depends(get_my_info)):

    if not payload or payload["type"] != "Doctor":
        raise credentials_exception

