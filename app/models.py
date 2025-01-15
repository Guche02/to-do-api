from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
import uuid

class User(Base):
    
    __tablename__ = 'User'
    id = Column(String(55), primary_key=True, default=lambda: str(uuid.uuid4())) 
    username= Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    todos = relationship("Todo",back_populates="owner")
    
class Todo(Base):
    __tablename__ = "Todo"
    id = Column(String(55), primary_key=True, default=lambda: str(uuid.uuid4())) 
    title = Column(String(255), index=True)
    user_id = Column(String(55), ForeignKey("User.id"))
    owner = relationship("User",back_populates="todos")
    