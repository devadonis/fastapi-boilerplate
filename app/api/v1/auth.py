from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.internal.dependencies import get_db
from app.internal.auth import authenticate, create_access_token
from app.crud.schemas import UserCreate, Token
from app.crud import auth
from app.db.database import engine
from app.db import models


models.Base.metadata.create_all(bind=engine)
router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """Get the JWT for a user with data from OAuth2 request form body"""
    user = authenticate(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password.")

    token_data = {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }
    token = Token(**token_data)

    return token


@router.post("/signup", response_model=Token)
def signup(*, db: Session = Depends(get_db), user_data: UserCreate) -> Any:
    """Create new user with login"""
    user = auth.get_user_by_email(db=db, email=user_data.email)

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    new_user = auth.sign_up(db=db, user_data=user_data)

    token_data = {
        "access_token": create_access_token(sub=new_user.id),
        "token_type": "bearer",
    }
    token = Token(**token_data)

    return token
