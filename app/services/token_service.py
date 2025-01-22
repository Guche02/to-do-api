import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
# Retrieve values from the environment

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))  # Default to 30 if not set
SECRET_KEY = os.getenv("SECRET_KEY")  
ALGORITHM = os.getenv("ALGORITHM")  

def create_access_token(data: dict):
    print(f"encoding value taken {data}")
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    print(expire)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print("Encoded")
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check if the token has expired
        if payload["exp"] < datetime.utcnow().timestamp():
            print("manual exp error caught")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        return payload
    except jwt.ExpiredSignatureError:
        print("Exp error caught")
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.JWTError:
        print("JWT error caught")
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
