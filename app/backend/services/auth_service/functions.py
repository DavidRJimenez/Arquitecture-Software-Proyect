from sqlalchemy.orm import Session
from models import User


def create_user(user: User, db: Session) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
