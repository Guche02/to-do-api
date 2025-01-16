from ..services.todo_services import create_todo_serive, update_todo_service, get_todo_service, get_user_todo_service
from sqlalchemy.orm import Session

async def create_todo_controller(user_id,todo,db:Session):
    print(f"controller:{todo}")
    todo = await create_todo_serive(user_id,todo,db)
    return todo

async def update_todo_controller(task_id,todo,db:Session):
    print(f"controller:{todo}")
    todo = await update_todo_service(task_id,todo,db)
    return todo

async def get_todo_controller(db:Session):
    print("controller getting todo")
    todo = await get_todo_service(db)
    return todo

async def get_user_todo_controller(user_id,db):
    todo = await get_user_todo_service(user_id,db)
    print(f"user's todos {todo}")
    return todo

