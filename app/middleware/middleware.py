from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from ..services.token_service import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
open_route = "/open"  
class ValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(open_route):
            return await call_next(request)
        try:
            token = await oauth2_scheme(request) 
            user = decode_token(token)  
            request.state.payload = user
            response = await call_next(request) 
            return response
        except HTTPException as exc:
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
        except Exception as exc:
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
        
        