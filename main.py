import uvicorn
from fastapi import FastAPI

from src.resources.add_user import add_user_router
from src.resources.anonymous_venting import anonymous_venting_router
from src.resources.change_password import change_pass_router
from src.resources.forget_password import forget_password_router
from src.resources.therapist_info import therepist_info_router
from src.resources.token import token_router

app = FastAPI()

"""
run from here
"""

app.include_router(token_router, prefix="/yeh-zindagi/api/user/token")
app.include_router(add_user_router, prefix="/yeh-zindagi/api/user/sign-up")
app.include_router(change_pass_router, prefix="/yeh-zindagi/api/user/change-pass")
app.include_router(forget_password_router, prefix="/yeh-zindagi/api/user/forget_password")
app.include_router(therepist_info_router, prefix="/yeh-zindagi/api/therapist")
app.include_router(anonymous_venting_router, prefix="/yeh-zindagi/api/vent")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
