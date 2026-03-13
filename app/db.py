from sqlalchemy import Engine
from sqlmodel import SQLModel

from app.config.settings import settings

postgresql_url = settings.DB_URL
def create_db_and_tables(engine: Engine):
    SQLModel.metadata.create_all(engine)
