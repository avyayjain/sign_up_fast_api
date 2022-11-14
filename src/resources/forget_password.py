from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.common.utils.generate_error_details import generate_details
from src.common.utils.user_defined_errors import UserErrors
from src.db.functions.forget_password import forget_user

forget_password_router = APIRouter()


class AuthAddUser(BaseModel):
    email: str
    password: str
    resource_id: str


@forget_password_router.post("")
async def forget_password(
        form_data: AuthAddUser
):
    """
    API to ADD Users

    """
    try:
        forget_user(user_email=form_data.email, password=form_data.password, user_id=form_data.resource_id)
        return {"detail": "User Password Updated"}
    except UserErrors as e:
        data = "\n User Email {}  \n password {} \n ".format(
            str(form_data.email), str(form_data.password)
        )

        details = generate_details(e.message, e.type)

        raise HTTPException(status_code=e.response_code, detail=details)
    except Exception:
        data = "\n User Email {}  \n password {} \n ".format(
            str(form_data.email), str(form_data.password)
        )

        details = generate_details("Internal Server Error", "InternalServerError")
        raise HTTPException(status_code=500, detail=details)
