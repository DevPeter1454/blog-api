from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .database import get_db
from . import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password :str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(email: str, db:Session):
    return db.query(models.User).filter(models.User.email == email).first()

def user_to_dict(user):
    return {
        column.key: getattr(user, column.key)
        for column in user.__table__.columns
    }
    
def dict_to_user(user, data):
    for key, value in data.items():
        setattr(user, key, value)
    return user



def get_user_by_id(id: int, db:Session):
    return db.query(models.User).filter(models.User.id == id).first()

def get_blog_likes(db:Session, id: int):
    return db.query(models.UserBlogLikes).filter(models.UserBlogLikes.blog_id == id).all()