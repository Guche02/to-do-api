from ..services.user_servies import create_user_service,login_user_service
from sqlalchemy.orm import Session

async def create_user_controller(user,db:Session):
    print(f"controller: {user}")
    user =await  create_user_service(user,db)
    return user

async def login_user_controller(user,db:Session):
    print(f"controller{user}")
    token= await login_user_service(user,db)
    return token