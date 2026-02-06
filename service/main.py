from fastapi import FastAPI
from .database import engine
from . import models
from .router import service
from .router import users
#create table
models.Base.metadata.create_all(bind= engine)

app = FastAPI()

app.include_router(service.router)
app.include_router(users.router)



