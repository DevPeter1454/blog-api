from fastapi import FastAPI, status
from .routers import users, blogs, auth
from .database import engine
from . import models
from mangum import Mangum
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

handler = Mangum(app)

app.include_router(users.router)
app.include_router(blogs.router)
app.include_router(auth.router)



@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "server is running"}