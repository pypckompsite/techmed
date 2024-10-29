from datetime import datetime
from typing import Optional

from sqlmodel import create_engine, Session, SQLModel

from api.models import *

DATABASE_URL = "sqlite:///orm.db"
engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

def drop_db():
    SQLModel.metadata.drop_all(engine)
