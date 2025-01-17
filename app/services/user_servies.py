from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException,Depends
from ..models.models import User
from sqlalchemy.orm import Session
from ..database.db import SessionLocal
from bcrypt import checkpw
from .token_service import create_access_token


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
            password = user.password
        )
        # db_user.password = user.password
        print(f"user db created {db_user}")
        db.add(db_user)
        # print(db_user)
        db.commit()
        db.refresh(db_user)
        # print(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        if 'email' in str(e.orig):
            print(e.orig)
            raise HTTPException(
                status_code= 400,
                detail="Email is already in use."
            )
        print(e)
        raise HTTPException(status_code=400, detail="Database error ocurred.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An unexpected error occured")


async def login_user_service(user, db:Session):
    try:
        db_user = db.query(User).filter(User.email==user.email).first()
        print(db_user)
        if db_user is None:
            raise HTTPException(status_code=400, detail="User doesn't exist")
        
        if checkpw(user.password.encode('utf-8'), db_user._password.encode('utf-8')):
            print("Password verification passed")
            access_token = create_access_token({"user_id":db_user.id,"email": db_user.email,
                                                "username":db_user.username})
            print("Access token generated:", access_token)
            return {"access_token": access_token, "token_type": "bearer"}
        
        raise HTTPException(status_code=400, detail="Incorrect password")
            
    except IntegrityError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=400, detail="Database error ocurred.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An unexpected error occured")
             
             
             
