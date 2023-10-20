from fastapi import APIRouter, status, Depends, Response, HTTPException
from .. import schemas, models, utils
from sqlalchemy.orm import Session
from ..database import get_db



router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "server is running"}

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if utils.get_user_by_email(user.email, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/get/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user_by_id(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

