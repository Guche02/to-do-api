from fastapi import APIRouter
from ..controllers.user_controller import create_user_controller
from ..schemas.user_schema import UserCreate
router = APIRouter()

@router.post("/users/")
def create_user_route(user: UserCreate):
    return create_user_controller(user)
