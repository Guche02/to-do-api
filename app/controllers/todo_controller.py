from ..services.todo_services import create_todo_serive, update_todo_service, get_user_todo_service,delete_todo_service
from sqlalchemy.orm import Session

async def create_todo_controller(todo,db:Session, request):
    print(f"controller:{todo}")
    todo = await create_todo_serive(todo,db,request)
    return todo

async def update_todo_controller(request,task_id,todo,db:Session):
    print(f"controller:{todo}")
    todo = await update_todo_service(task_id,todo,db,request)
    return todo

async def get_user_todo_controller(request,db):
    todo = await get_user_todo_service(db,request)
    print(f"user's todos {todo}")
    return todo

async def delete_todo_controller(request,todo_id,db):
    message = await delete_todo_service(todo_id,db,request)
    print(f"user's todos {message}")
    return message
   