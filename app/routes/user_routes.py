from fastapi import APIRouter,Depends
from ..controllers.user_controller import create_user_controller, login_user_controller
from ..schemas.user_schema import UserCreate, UserLogin
from ..database.db import SessionLocal
from sqlalchemy.orm import Session
from bcrypt import checkpw

router = APIRouter()

def get_db():
    db = SessionLocal() 
    try :    
        yield db
    finally:
        db.close()
        
@router.post("/open/register/")
async def create_user_route(user: UserCreate ,db:Session=Depends(get_db)):
    print(user)
    user = await  create_user_controller(user,db)
    return user

@router.post("/open/login/")
async def login_user_route(user: UserLogin, db: Session=Depends(get_db)):
    token= await login_user_controller(user,db)
    return token


