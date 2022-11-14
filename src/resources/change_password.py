from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.db.functions.logout import user_logout
from src.db.functions.update_password import update_pass
from src.resources.token import UserBase, get_current_active_user

change_pass_router = APIRouter()


class PassUser(BaseModel):
    new_password: str


@change_pass_router.post("")
async def login_for_access_token(
    form_data: PassUser, current_user: UserBase = Depends(get_current_active_user)
):
    """
    API to change password

    """
    try:
        update_pass(user_email=current_user.email, password=form_data.new_password)
    except Exception as e:
        print(e)

    try:
        user_logout(current_user.email)
    except Exception as e:
        print(e)

    return {"detail": "Password Changed"}