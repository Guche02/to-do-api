from pydantic import BaseModel, EmailStr

class TodoBase(BaseModel):
    title : str    
    
class TodoUpdate(BaseModel):
    status : bool    
 
class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id : str
    owner_id  : str
    class Config:
        orm_mode = True
        
class TodoRead(TodoBase):
    id: int
    title: str  
    status: bool

    class Config:
        orm_mode = True  
