from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from src.common.utils.generate_error_details import generate_details
from src.common.utils.pwd_helper import verify_password
from src.common.utils.constants import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM,
)
from src.common.utils.user_defined_errors import UserErrors, PermissionDeniedError
from src.db.errors import ItemNotFound
from src.db.functions.find_user import find_user_pass
from src.db.functions.logout import user_login, user_logout

token_router = APIRouter()


class AuthUser(BaseModel):
    username: str
    password: str


class LogoutUser(BaseModel):
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    email: str
    disabled: Optional[bool] = None
    logout: Optional[bool] = None
    user_id: str


class UserInDB(UserBase):
    hashed_password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(user_email: str):
    """
    :param user_email: User Email
    """
    try:
        hash_pass, disable_status, logout, user_id = find_user_pass(user_email)
    except UserErrors:
        raise
    except Exception:
        raise
    return UserInDB(
        user_id=user_id,
        email=user_email,
        diable=disable_status,
        hashed_password=hash_pass,
        logout=logout,
    )


def authenticate_user(user_email: str, password: str):
    """

    :param user_email: User Email
    @type user_email: str
    :param password: User Password
    @type password: str
    @return: User Object
    @rtype: object
    """
    try:
        hash_pass, disable_status, logout, user_id = find_user_pass(user_email)
    except ItemNotFound:
        return False
    except UserErrors:
        raise
    except:
        return False
    if not verify_password(password, hash_pass):
        return False
    return UserInDB(
        user_id=user_id,
        email=user_email,
        diable=disable_status,
        hashed_password=hash_pass,
        logout=logout,
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
        This function is use to create access token

        @param data: Data required to for jwt creation
        @type data: Dict
        @param expires_delta: expiry time
        @type expires_delta: timedelta
        @return: encoded token
        @rtype: str
        """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """

        @param token: token is used to check credentials
        @type token: str
        @return: user object
        @rtype: object
        """

    details = generate_details(
        "Could not validate credentials", "PermissionDeniedError"
    )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=details,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise PermissionDeniedError
        token_data = TokenData(email=email)
    except UserErrors as e:
        try:
            data = "\n User Email {}".format(str(email))
        except Exception as e:
            print(e)

        raise HTTPException(status_code=e.response_code, detail=details)

    except JWTError:
        try:
            data = "\n User Email {}".format(str(email))
        except:
            data = "\n User Email {}".format("Can't Access Email")

        raise credentials_exception

    except Exception:
        try:
            data = "\n User Email {}".format(str(email))
        except:
            data = "\n User Email {}".format("Can't Access Email")

        raise credentials_exception
    try:
        user = get_user(user_email=token_data.email)
    except UserErrors as e:
        data = "\n User Email {}".format(str(email))

        details = generate_details(e.message, e.type)

        raise HTTPException(status_code=e.response_code, detail=details)
    except:
        data = "\n User Email {}".format(str(email))

        raise credentials_exception
    if user is None:
        data = "\n User Email {}".format(str(email))

        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserBase = Depends(get_current_user)):
    """

        @param current_user: User Object
        @type current_user: Object
        @return: User Object
        @rtype: Object
        """
    if current_user.disabled:
        details = generate_details("Inactive user", "ForbiddenUserError")
        data = "\n User Email {} , Disabled User".format(str(current_user.email))

        raise HTTPException(status_code=403, detail=details)
    if current_user.logout:
        details = generate_details("User Logout. Login Again", "LogoutUserError")
        data = "\n User Email {} , Logout User Error".format(str(current_user.email))

        raise HTTPException(status_code=401, detail=details)
    return current_user


@token_router.post("", response_model=Token)
async def login_for_access_token(form_data: AuthUser):
    """
        API For Token Authorisationusername

    """
    try:
        user = authenticate_user(form_data.username, form_data.password)
    except UserErrors as e:
        data = "\n User Email {} , Logout User Error".format(str(form_data.username))

        details = generate_details(e.message, e.type)

        raise HTTPException(status_code=e.response_code, detail=details)
    except Exception:
        data = "\n User Email {} , Logout User Error".format(str(form_data.username))

        details = generate_details(
            "Incorrect Email or password", "PermissionDeniedError"
        )

        raise HTTPException(status_code=401, detail=details)
    if not user:
        details = generate_details(
            "Incorrect Email or password", "PermissionDeniedError"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=details,
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_login(user.email)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@token_router.post("/logout")
async def logout_endpoint(current_user: UserBase = Depends(get_current_active_user)):
    """
        API For Token Authorisation

        """

    if not current_user:
        details = generate_details(
            "Incorrect Email or password", "PermissionDeniedError"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=details,
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user_logout(current_user.email)
    except UserErrors as e:
        data = "\n User Email {}  \n ".format(str(current_user.email))

        details = generate_details(e.message, e.type)

        raise HTTPException(status_code=e.response_code, detail=details)
    except Exception:
        data = "\n User Email {}  \n ".format(str(current_user.email))

        details = generate_details("Internal Server Error", "InternalServerError")
        raise HTTPException(status_code=500, detail=details)

    return {"message": "success"}
