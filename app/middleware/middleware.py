from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from ..services.token_service import decode_token
from ..models.models import Todo
from sqlalchemy.orm import Session
from typing import List
from ..database.db import SessionLocal


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
open_routes = ["/open"]  

class ValidationMiddleware(BaseHTTPMiddleware):
    print("middleware reached")
    
    async def dispatch(self, request: Request, call_next):
        print(f"request received {request}")

        if any(request.url.path.startswith(route) for route in open_routes):
            print("open route called")
            return await call_next(request)
        try:
            print("authenticating...")
            token = await oauth2_scheme(request) 
            user = decode_token(token)  
            request.state.payload = user
            print("authentication success")
            response = await call_next(request) 
            return response

        except HTTPException as exc:
            print(f"error {exc.detail}")
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)

        except Exception as exc:
            print(f"error {exc}")
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)