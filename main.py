import uvicorn
from fastapi import FastAPI

from src.resources.add_user import add_user_router
from src.resources.change_password import change_pass_router
from src.resources.forget_password import forget_password_router
from src.resources.token import token_router

app = FastAPI()

app.include_router(token_router, prefix="/translator-signup/api/editor/translator/v1/token")
app.include_router(add_user_router, prefix="/translator-signup/api/editor/translator/v1/sign-up")
app.include_router(change_pass_router, prefix="/translator-signup/api/editor/translator/v1/change-pass")
app.include_router(forget_password_router, prefix="/translator-signup/api/word-counter/admin/v1/forget_password")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8005,reload=True)
