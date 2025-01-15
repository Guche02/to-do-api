from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException,Depends

from ..models.models import User
# from ..schemas.user_schema import 
from ..database.db import SessionLocal
#Dependency
def get_db():
    db = SessionLocal() 
    try :    
        yield db
    finally:
        db.close()

def create_user_service( user,db: Session = Depends(get_db)):
    try:
        print(user)
        db_user = User(
            email=user.email,
            username=user.username,
            password=user.password  
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database error ocurred.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occured")
    
def get_user_by_email(email: str,db: Session = Depends(get_db)):
    return db.query(User).filter(User.email == email).first()
