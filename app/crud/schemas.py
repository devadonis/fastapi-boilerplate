from typing import Optional
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    text: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: Optional[int] = None


class UserInDB(UserInDBBase):
    hashed_password: str


class User(UserInDBBase):
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
