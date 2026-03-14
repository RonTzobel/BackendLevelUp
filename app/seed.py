"""
Demo account seeding.

Runs automatically on every backend startup (idempotent).
Creates two accounts if they don't already exist:
  - demo@levelup.com  / demo123  → role: user
  - admin@levelup.com / admin123 → role: admin
"""
import logging
from sqlalchemy import Engine
from sqlmodel import Session, select

from app.models.users import User, UserRole, UserStatus
from app.utilities.passwords import get_password_hash

logger = logging.getLogger(__name__)

_DEMO_ACCOUNTS = [
    {
        "email": "demo@levelup.com",
        "password": "demo123",
        "name": "Demo User",
        "role": UserRole.USER,
    },
    {
        "email": "admin@levelup.com",
        "password": "admin123",
        "name": "Demo Admin",
        "role": UserRole.ADMIN,
    },
]


def seed_demo_accounts(engine: Engine) -> None:
    """Create demo accounts if they do not already exist."""
    with Session(engine) as session:
        for account in _DEMO_ACCOUNTS:
            existing = session.exec(
                select(User).where(User.email == account["email"])
            ).first()

            if existing:
                # Ensure role and active status are correct even if the row was modified.
                changed = False
                if existing.role != account["role"]:
                    existing.role = account["role"]
                    changed = True
                if existing.status != UserStatus.ACTIVE:
                    existing.status = UserStatus.ACTIVE
                    changed = True
                if changed:
                    session.add(existing)
                    logger.info("Updated demo account: %s", account["email"])
                else:
                    logger.info("Demo account already exists: %s", account["email"])
                continue

            user = User(
                email=account["email"],
                password=get_password_hash(account["password"]),
                name=account["name"],
                role=account["role"],
                status=UserStatus.ACTIVE,
            )
            session.add(user)
            logger.info(
                "Created demo account: %s (role=%s)", account["email"], account["role"]
            )

        session.commit()
