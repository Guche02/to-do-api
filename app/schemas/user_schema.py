from pydantic import BaseModel, EmailStr
from .todo_schema import Todo

class UserBase(BaseModel):
    email: EmailStr
    username: str
    
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id : str
    todos : list[Todo] = []
    class Config:
        orm_model = True

class UserRead(UserBase):
    id: int
    username: str  
    email: str

    class Config:
        orm_mode = True  
