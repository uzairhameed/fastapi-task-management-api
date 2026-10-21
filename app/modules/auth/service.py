
from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.modules.users.models import User
from app.modules.auth.schemas import Token


def login_user(db: Session, username: str, password: str) -> Token:
    user = db.scalar(
        select(User).where(User.username == username)
    )

    if user is None or not verify_password(
        password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=timedelta(minutes=30),
    )

    return Token(access_token=access_token)
