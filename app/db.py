import os

from sqlalchemy import Engine
from sqlmodel import SQLModel

# Use environment variable if available (for Docker), otherwise use localhost
postgresql_url = os.getenv(
    "DATABASE_URL",
    default="postgresql://Almog:1999@127.0.0.1:5432/levelup"
)

print("db=" , postgresql_url)
def create_db_and_tables(engine: Engine):
    SQLModel.metadata.create_all(engine)
