import os

from sqlalchemy import Engine
from sqlalchemy import text
from sqlmodel import SQLModel

# Use DATABASE_URL if set (e.g. Docker/PostgreSQL), otherwise SQLite for local dev (no install needed)
postgresql_url = os.getenv(
    "DATABASE_URL",
    default="sqlite:///./levelup.db"
)


def _sqlite_ensure_users_preferences_columns(engine: Engine) -> None:
    """
    Lightweight dev-only migration for SQLite.
    SQLModel's create_all() doesn't alter existing tables, so if the local
    `levelup.db` was created before preference columns existed, update endpoints
    would crash. This safely adds missing columns if needed.
    """
    if engine.url.get_backend_name() != "sqlite":
        return

    with engine.begin() as conn:
        columns = [row[1] for row in conn.execute(text("PRAGMA table_info('users')")).fetchall()]

        if "favorite_genre" not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN favorite_genre VARCHAR(255)"))

        if "preferred_store" not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN preferred_store VARCHAR(255)"))


def create_db_and_tables(engine: Engine) -> None:
    SQLModel.metadata.create_all(engine)
    _sqlite_ensure_users_preferences_columns(engine)
