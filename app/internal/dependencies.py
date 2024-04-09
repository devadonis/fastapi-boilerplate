from typing import Generator

from app.db.database import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    except:
        db.rollback()
    finally:
        db.close()
