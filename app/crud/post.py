from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db import models
from app.crud.schemas import PostCreate


def create_post(db: Session, post_data: PostCreate, owner_id: int):
    try:
        conn = db
        post = models.Post(text=post_data.text, owner_id=owner_id)
        conn.add(post)
        conn.commit()
        conn.refresh(post)

        post_id = post.id

        return post_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DataBase Error: {str(e)}")


def get_all_posts(db: Session):
    try:
        conn = db
        posts = conn.query(models.Post).all()

        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DataBase Error: {str(e)}")


def get_post_by_id(db: Session, post_id: int):
    try:
        conn = db
        result = conn.query(models.Post).filter(models.Post.id == post_id).first()
        post = result if result else None

        return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DataBase Error: {str(e)}")


def delete_post_by_id(db: Session, post_id: int):
    try:
        conn = db
        conn.query(models.Post).filter_by(id=post_id).delete()
        conn.commit()

        return {"message": "Successfully delete the post."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DataBase Error: {str(e)}")
