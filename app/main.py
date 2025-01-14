from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from .db import SessionLocal, engine
from pydantic import BaseModel
from . import crud,models, schemas

app = FastAPI()
models.Base.metadata.create_all(bind=engine)



#Dependency
def get_db():
    db = SessionLocal() 
    try :    
        yield db
    finally:
        db.close()

db_dependency = Annotated(Session, Depends(get_db))

@app.post("/users/",response_model=schemas.User)
def post_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    # db_user = crud.get_user_by_email(db, email=user.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db,user=user)