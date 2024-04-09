from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import BaseModel

from app.core.config import settings
from app.internal.auth import oauth2_scheme
from app.crud.schemas import UserInDBBase
from app.crud import auth
from app.db.database import SessionLocal


class TokenData(BaseModel):
    id: Optional[str] = None


def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    except:
        db.rollback()
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> UserInDBBase:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    user = auth.get_user_by_id(db=db, id=token_data.id)

    if user is None:
        raise credentials_exception

    return user
