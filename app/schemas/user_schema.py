from pydantic import BaseModel, EmailStr
from .todo_schema import Todo

class UserBase(BaseModel):
    email: EmailStr
     
class UserCreate(UserBase):
    username: str
    password: str
    
class UserLogin(UserBase):
    email: EmailStr
    password: str    

class User(UserBase):
    id : str
    todos : list[Todo] = []
    class Config:
        orm_model = True

