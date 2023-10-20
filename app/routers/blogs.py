from fastapi import APIRouter, status, Depends, Response, HTTPException
from .. import schemas, models, utils , oauth2
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db



router = APIRouter(
    prefix="/blogs",
    tags=["blogs"]
)

@router.get("/", status_code=status.HTTP_200_OK, )
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if len(blogs) == 0:
        return []
    all_blogs = []
    
    for blog in blogs:
        owner = utils.user_to_dict(utils.get_user_by_id(blog.user_id, db))
        # likes = utils.get_blog_likes(db, blog.id)
        # print(likes)
        del owner['password']
        del owner['created_at']
        del owner['updated_at']
        del owner['id']
        all_blogs.append({
            "blog": blog,
            "author": owner
        })
    return all_blogs

@router.post("/create", status_code=status.HTTP_201_CREATED, )
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    print(utils.user_to_dict(current_user))
    user = utils.user_to_dict(current_user)
    del user['password']
    new_blog = models.Blog(**blog.model_dump())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {
        "message": "blog created successfully",
        "blog": new_blog,
        "user": user
    }


@router.put("/edit/{id}", status_code=status.HTTP_202_ACCEPTED)
def edit_blog(id: int, blog: schemas.BlogCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(blog.model_dump())
    db.commit()
    return {
        "message": "blog updated successfully",
        "blog": blog.first()
    }
    

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {
        "message": "blog deleted successfully",
    }
    
# @router.post("/like/{id}", status_code=status.HTTP_202_ACCEPTED)
# def like_blog_post(id:int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
#     blog = db.query(models.UserBlogLikes).filter(models.UserBlogLikes.blog_id == id).filter(models.UserBlogLikes.user_id == current_user.id)
#     if blog.first():
#          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog already liked")
#     new_like = models.UserBlogLikes(user_id = current_user.id, blog_id = id)
#     db.add(new_like)
#     db.commit()
#     db.refresh(new_like)
#     return {
#         "message": "blog liked successfully",
#         "like": new_like
#     }