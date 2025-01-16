from fastapi import APIRouter,Depends
from ..controllers.user_controller import create_user_controller
from ..schemas.user_schema import UserCreate
from ..database.db import SessionLocal
from sqlalchemy.orm import Session
router = APIRouter()

def get_db():
    db = SessionLocal() 
    try :    
        yield db
    finally:
        db.close()
        
@router.post("/users/")
async def create_user_route(user: UserCreate ,db:Session=Depends(get_db)):
    print(user)
    user = await  create_user_controller(user,db)
    return user
