from pydantic import BaseModel, EmailStr

class TodoBase(BaseModel):
    title : str    
class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id : str
    owner_id  : str
    class Config:
        orm_mode = True
