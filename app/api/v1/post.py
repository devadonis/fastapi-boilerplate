from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm.session import Session
from cachetools import TTLCache

from app.internal.dependencies import get_db, get_current_user
from app.crud.schemas import Post, PostCreate, User
from app.crud import post


router = APIRouter()
cache = TTLCache(maxsize=100, ttl=300)


@router.post("/", response_model=int)
def create_post(
    *,
    post_data: PostCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new post"""
    # check content length to not exceed 1MB
    if request.headers.get("content-length"):
        content_length = int(request.headers.get("content-length"))
        if content_length > 1000000:
            raise HTTPException(status_code=413, detail="Payload too large")

    post_id = post.create_post(db=db, post_data=post_data, owner_id=current_user.id)

    return post_id


@router.get("/", response_model=List[Post])
def get_posts(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Get all posts"""
    user_id = current_user.id

    # check the cache first
    if user_id in cache:
        return cache[user_id]

    # if not in cache, fetch posts and update cache
    posts = post.get_all_posts(db=db)
    cache[user_id] = posts

    return posts


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a post by post id"""
    # check the user to delete the post
    post_data = post.get_post_by_id(db=db, post_id=post_id)
    if not post_data:
        raise HTTPException(status_code=400, detail=f"Can't find the current post.")

    if post_data.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"You can only delete your posts.")

    result = post.delete_post_by_id(db=db, post_id=post_id)

    return result
