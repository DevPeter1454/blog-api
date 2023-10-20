from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional



class User(BaseModel):
    email: EmailStr
    first_name : str
    last_name : str
    
        
class UserCreate(User):
    password: str


class UserOut(User):
    id: int
    created_at:datetime
    updated_at:datetime
    class Config:
        from_attributes = True
        
class Blog(BaseModel):
    title: str
    body: str
    user_id: int
    banner_image : str
    is_published : bool = False
    
class BlogOut(Blog):
    id: int
    created_at:datetime
    updated_at:datetime
    class Config:
        from_attributes = True
        
        
class BlogCreate(Blog):
    pass


class UserBlogLikes(BaseModel):
    user_id: int
    blog_id: int
    
class UserLogin(BaseModel):
    email: EmailStr
    password : str
    
class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None
    email : Optional[EmailStr] = None
