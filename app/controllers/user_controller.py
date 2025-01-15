from ..services.user_servies import create_user_service

def create_user_controller(user):
    return create_user_service(user)