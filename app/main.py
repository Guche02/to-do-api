from fastapi import FastAPI
from .models import models
from .database.db import engine
from .routes.user_routes import router as user_router  
from .routes.todo_routes import router as todo_router
from .middleware.middleware import ValidationMiddleware

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
app.include_router(todo_router)

app.add_middleware(ValidationMiddleware)