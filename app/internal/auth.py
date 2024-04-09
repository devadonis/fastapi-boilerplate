from typing import Optional
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from jose import jwt

from app.core.config import settings
from app.internal.security import verify_password
from app.crud.schemas import User
from app.crud import auth


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def authenticate(*, email: str, password: str, db: Session) -> Optional[User]:
    # get user by email
    user = auth.get_user_by_email(db, email=email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def create_access_token(*, sub: str) -> str:
    payload = {}
    lifetime = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + lifetime

    payload["type"] = str("access_token")

    # The "exp" (expiration time) claim identifies the expiration time on
    # or after which the JWT must not be accepted for processing
    payload["exp"] = expire

    # The "iat" (issued at) claim identifies the time at which the JWT was issued
    payload["iat"] = datetime.now(timezone.utc)

    # The "sub" (subject) claim identifies the principal that is the subject of the JWT
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
