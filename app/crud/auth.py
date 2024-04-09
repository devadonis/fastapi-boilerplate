from pydantic import EmailStr

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db import models
from app.crud.schemas import UserCreate
from app.internal.security import get_password_hash


def get_user_by_email(db: Session, email: EmailStr):
    try:
        conn = db
        result = conn.query(models.User).filter(models.User.email == email).first()
        user = result if result else None

        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DataBase Error: {str(e)}")


def get_user_by_id(db: Session, id: int):
    try:
        conn = db
        result = conn.query(models.User).filter(models.User.id == id).first()
        user = result if result else None

        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DataBase Error: {str(e)}")


def sign_up(db: Session, user_data: UserCreate):
    try:
        conn = db
        user = models.User(
            email=user_data.email, hashed_password=get_password_hash(user_data.password)
        )
        conn.add(user)
        conn.commit()
        conn.refresh(user)

        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DataBase Error: {str(e)}")
