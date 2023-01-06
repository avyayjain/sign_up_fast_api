from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.db.functions.add_user import create_user
from src.db.functions.logout import user_logout
from src.resources.token import UserBase, get_current_active_user

add_user_router = APIRouter()


class AuthAddUser(BaseModel):
    email: str
    password: str
    name: str


class DeleteUser(BaseModel):
    email: str


@add_user_router.post("")
async def sign_up(
    form_data: AuthAddUser
):
    """
    API to ADD Users

    """
    try:
        create_user(
            user_name=form_data.name,
            user_email=form_data.email,
            password=form_data.password,

        )
        return {"detail": "User Added"}
    except Exception as e:
        print(e,"error")


@add_user_router.delete("")
async def delete_user(
    form_data: DeleteUser, current_user: UserBase = Depends(get_current_active_user)
):
    """
    API to ADD Users
    """
    try:
        try:
            user_logout(form_data.email)
        except Exception as e:
            print(e)
        return {"detail": "User Delete"}

    except Exception as e:
        print(e)
