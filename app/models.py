from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
    
class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    banner_image = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
    
class UserBlogLikes(Base):
    __tablename__ = 'user_blog_likes'
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    blog_id = Column(Integer, ForeignKey('blogs.id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)