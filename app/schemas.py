from pydantic import BaseModel

class TodoBase(BaseModel):
    title : str    
class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id : str
    owner_id  : str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str
    password: str
class UserCreate(UserBase):
    pass 

class User(UserBase):
    id : str
    todos : list[Todo] = []

    class Config:
        orm_model = True
