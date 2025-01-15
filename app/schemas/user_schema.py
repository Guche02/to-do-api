from pydantic import BaseModel, EmailStr
from .todo_schema import Todo

class UserBase(BaseModel):
    email: EmailStr
    username: str
    password: str
class UserCreate(UserBase):
    pass 

class User(UserBase):
    id : str
    todos : list[Todo] = []

    class Config:
        orm_model = True
