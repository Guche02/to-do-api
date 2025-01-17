from fastapi import APIRouter,Depends
from ..controllers.todo_controller import create_todo_controller,update_todo_controller,get_todo_controller, get_user_todo_controller, delete_todo_controller
from ..schemas.todo_schema import TodoCreate,TodoUpdate
from ..database.db import SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal() 
    try :    
        yield db
    finally:
        db.close()

@router.post("/add_todo/")
async def create_todo_route(todo:TodoCreate,db:Session= Depends(get_db),user_token:str=  Depends(oauth2_scheme)):
    print(todo)
    todo=await create_todo_controller(user_token,todo,db)
    return todo

@router.patch("/update_todo/{task_id}")
async def update_todo_route(task_id:str,todo:TodoUpdate,db:Session= Depends(get_db),user_token:str=Depends(oauth2_scheme)):
    print(todo)
    todo=await update_todo_controller(user_token,task_id,todo,db)
    return todo

@router.get("/get_todo/")
async def get_todo_route(db:Session= Depends(get_db)):
    todo=await get_todo_controller(db)
    return todo

@router.get("/get_user_todo/{user_id}")
async def get_user_todo(user_id:str,db:Session= Depends(get_db)):
    todo = await get_user_todo_controller(user_id,db)
    return todo

@router.delete("/delete_todo/{todo_id}")
async def delete_todo(todo_id:str, db: Session = Depends(get_db),user_token:str=Depends(oauth2_scheme)):
    message = await delete_todo_controller(user_token,todo_id,db)
    return message