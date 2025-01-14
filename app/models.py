from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    
    __tablename__ = 'User'
    id= Column(Integer, primary_key=True, index=True,default=generate_uuid)
    username= Column(String(50))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    todos = relationship("Todo",back_populates="owner")
    
class Todo(Base):
    __tablename__ = "Todo"
    id = Column(Integer, primary_key=True, index=True,default=generate_uuid)
    title = Column(String(255), index=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    owner = relationship("User",back_populates="Todo")
    