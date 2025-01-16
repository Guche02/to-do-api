from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .schemas import user_schema

from .models import models
from .database.db import engine
from pydantic import BaseModel
from .services import user_servies
from .routes.user_routes import router as user_router  
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

import logging
import sys

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

@app.get("/")
def root():
   logger.debug('this is a debug message')
   print("root route")
   return {"message": "Hello World"}

app.include_router(user_router)