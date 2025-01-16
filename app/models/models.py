from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database.db import Base
import uuid
from passlib.hash import bcrypt

class User(Base):
    __tablename__ = 'User'
    id = Column(String(55), primary_key=True, default=lambda: str(uuid.uuid4())) 
    username= Column(String(255))
    email = Column(String(255), unique=True, index=True)
    _password = Column("password", String(255), nullable=False)
    todos = relationship("Todo",back_populates="owner")

    @property
    def password(self):
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, raw_password):
        self._password = bcrypt.hash(raw_password)
    
class Todo(Base):
    __tablename__ = "Todo"
    id = Column(String(55), primary_key=True, default=lambda: str(uuid.uuid4())) 
    title = Column(String(255), index=True)
    user_id = Column(String(55), ForeignKey("User.id"))
    owner = relationship("User",back_populates="todos")
    