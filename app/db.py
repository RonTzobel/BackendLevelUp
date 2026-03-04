import os

from sqlalchemy import Engine
from sqlmodel import SQLModel

postgresql_url = os.getenv("DATABASE_URL")


def create_db_and_tables(engine: Engine) -> None:
    SQLModel.metadata.create_all(engine)
