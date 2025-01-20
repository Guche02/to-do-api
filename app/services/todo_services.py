from sqlalchemy.orm import Session
from ..models.models import Todo
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Request

import jwt

        
async def create_todo_serive(todo,db:Session,request):
    try:
        user = request.state.payload
        print(f"used passed to create todo {user}")
        db_todo = Todo(
            title=todo.title,
            user_id=user.get("user_id")
        )
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except IntegrityError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=400, detail="Database error ocurred.")
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An unexpected error occured")
        
async def update_todo_service(task_id,todo,db:Session, request):
    try:
        db_todo=db.query(Todo).filter(Todo.id==task_id).first()
        
        if db_todo is None:
            print("todo not found this")
            raise HTTPException(status_code=404, detail="Todo not found")
        
        user = request.state.payload
        if user.get("user_id")!=db_todo.user_id:
            raise HTTPException(status_code=404, detail="Unauthorized access")
        
        if todo.status:
            db_todo.status=todo.status
            
        db.commit()
        db.refresh(db_todo)
        
        return db_todo
    
    except IntegrityError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=400,detail="Database error occurred") 
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")   
    

async def get_user_todo_service( db: Session, request ):
    try:
        user = request.state.payload
        todos = db.query(Todo).filter(Todo.user_id == user.get("user_id")).all()
        print(todos)
        if not todos:
            raise HTTPException(status_code=404, detail="Todos not found for this user.")
        return todos
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while fetching todos for the user.")

async def delete_todo_service(todo_id: int, db: Session,request):
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found.")
        user = request.state.payload
        if user.get("user_id")!=todo.user_id:
            raise HTTPException(status_code=404, detail="Unauthorized access")
        db.delete(todo)
        db.commit()
        return {"detail": f"Todo with ID {todo_id} has been successfully deleted."}
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the todo.")

    
