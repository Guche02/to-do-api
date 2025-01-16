
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException,Depends

from ..models.models import User
# from ..schemas.user_schema import 
from sqlalchemy.orm import Session
from ..database.db import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal() 
    try :    
        yield db
    finally:
        db.close()

async def create_user_service( user,db: Session):
    try:
        print(f"servie {user}")
        db_user = User(
            username=user.username,
            email=user.email,
            password=user.password  
        )
        # print(db_user)
        db.add(db_user)
        # print(db_user)
        db.commit()
        db.refresh(db_user)
        # print(db_user)
        return db_user
    except IntegrityError as e:
        await db.rollback()
        if 'email' in str(e.orig):
            raise HTTPException(
                status_code= 400,
                detail="Email is already in use."
            )
        print(e)
        raise HTTPException(status_code=400, detail="Database error ocurred.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An unexpected error occured")
    
# def get_user_by_email(email: str,db: Session = Depends(get_db)):
#     return db.query(User).filter(User.email == email).first()
