from fastapi import APIRouter,Depends, Request
from ..controllers.todo_controller import create_todo_controller,update_todo_controller, get_user_todo_controller, delete_todo_controller
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
async def create_todo_route(todo:TodoCreate,request: Request,db:Session= Depends(get_db)):
    print(todo)
    todo=await create_todo_controller(todo,db,request)
    return todo

@router.patch("/update_todo/{task_id}")
async def update_todo_route(task_id:str,todo:TodoUpdate,request:Request,db:Session= Depends(get_db)):
    print(todo)
    todo=await update_todo_controller(request,task_id,todo,db)
    return todo

@router.get("/get_user_todo/")
async def get_user_todo(request:Request,db:Session= Depends(get_db)):
    todo = await get_user_todo_controller(request,db)
    return todo

@router.delete("/delete_todo/{todo_id}")
async def delete_todo(todo_id:str,request:Request, db: Session = Depends(get_db)):
    message = await delete_todo_controller(request,todo_id,db)
    return message