from datetime import datetime
from typing import Optional

from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = "sqlite:///orm.db"
engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
