
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

"""
__tablename__ = "users" sets the PostgreSQL table name.
- Mapped[int] and Mapped[str] are SQLAlchemy 2.x type annotations.
- mapped_column() defines the database columns.
- primary_key=True identifies the user's unique ID.
- unique=True prevents duplicate usernames or email addresses at the database level.
- nullable=False means the column cannot contain NULL.
- default=True sets the default value for is_active when SQLAlchemy inserts a user without an explicit value
- The index=True arguments request indexes to support lookups. Unique columns also have database uniqueness enforcement

"""
class User(Base):
    __tablename__ = "users"


    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
