import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from dotenv import load_dotenv

load_dotenv()
import os
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data: dict):
    print(f"encoding value taken {data}")
    expires_delta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
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

        if payload["exp"] < datetime.utcnow().timestamp():
            print("manaual exp error caught")
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
 