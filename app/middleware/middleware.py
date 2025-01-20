from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from ..services.token_service import decode_token
from ..models.models import Todo
from ..database.db import SessionLocal
# Define OAuth2PasswordBearer for extracting tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
open_routes = ["/open"]

# class ValidationMiddleware(BaseHTTPMiddleware):
#     print("middleware reached")
#     async def dispatch(self, request: Request, call_next):
#         # Define routes to skip token validation
#         print(f"request recived {request}")
#         if any(request.url.path.startswith(route) for route in open_routes):
#             print("open route called")
#             return await call_next(request)
#         db = self.get_db()
#         try:
#             # Use oauth2_scheme to extract the token
#             print("authenticating...")
#             token = await oauth2_scheme(request)  # Extracts the token from the Authorization header
#             user = decode_token(token)  # Validate the extracted token

#             # Proceed with the request if validation succeeds
#             print("authentication success")
            
#             # Task-specific validation for delete or update routes
#             if request.method in ["DELETE", "PUT"]:
#                 print(f"authorizing...")
#                 task_id = request.headers.get("Task-ID")
#                 if not task_id:
#                     raise HTTPException(status_code=400, detail="Task ID missing in headers")

#                 # Fetch the task from the database
#                 db_todo = db.query(Todo).filter(Todo.id == task_id).first()
#                 if not db_todo or db_todo.user_id != user.get("user_id"):
#                     raise HTTPException(status_code=403, detail="Unauthorized access to this task")
#                 print("authorization success")
#             response = await call_next(request) 
#             return response
            
#         except HTTPException as exc:
#             # Handle HTTP exceptions during validation
#             print(f"error {exc.detail}")
#             return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
#         except Exception as exc:
#             # Handle other exceptions
#             print(f"error {exc}")
#             return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
#         finally:
#             db.close()
            
#     @staticmethod
#     def get_db():
#         db = SessionLocal()
#         try:
#             yield db
#         finally:
#             db.close()        

class ValidationMiddleware(BaseHTTPMiddleware):
    print("middleware reached")
    
    def get_db(self):
        db = SessionLocal()  # Create a new database session
        return db

    async def dispatch(self, request: Request, call_next):
        print(f"request received {request}")
        
        # Define routes to skip token validation
        if any(request.url.path.startswith(route) for route in open_routes):
            print("open route called")
            return await call_next(request)

        # Get database session
        db = self.get_db()

        try:
            # Use oauth2_scheme to extract the token
            print("authenticating...")
            token = await oauth2_scheme(request)  # Extracts the token from the Authorization header
            user = decode_token(token)  # Validate the extracted token

            # Proceed with the request if validation succeeds
            print("authentication success")
            
            # Task-specific validation for delete or update routes
            if request.method in ["DELETE", "PUT"]:
                print(f"authorizing...")
                task_id = request.headers.get("Task-ID")
                if not task_id:
                    raise HTTPException(status_code=400, detail="Task ID missing in headers")

                # Fetch the task from the database
                db_todo = db.query(Todo).filter(Todo.id == task_id).first()
                if not db_todo or db_todo.user_id != user.get("user_id"):
                    raise HTTPException(status_code=403, detail="Unauthorized access to this task")
                print("authorization success")

            # Proceed with the request if all validation is successful
            response = await call_next(request) 
            return response

        except HTTPException as exc:
            # Handle HTTP exceptions during validation
            print(f"error {exc.detail}")
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)

        except Exception as exc:
            # Handle other exceptions
            print(f"error {exc}")
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)

        finally:
            db.close()  # Ensure the session is closed after the request