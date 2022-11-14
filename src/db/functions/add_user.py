from src.common.utils.constants import DB_CONNECTION_LINK
from src.common.utils.pwd_helper import get_password_hash
from src.db.database import Users
from src.db.errors import DataInjectionError, DatabaseErrors, DatabaseConnectionError
from src.db.utils import DBConnection


def create_user(user_email: str, password: str, user_id, disabled=False):
    """
    Add a Translator User

    :param user_id:
    :param user_email: User Email
    :param password: User Password
    :param disabled: Used to disable user
    :return: None
    """
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                user = Users(
                    email_id=user_email,
                    hashed_password=get_password_hash(password),
                    disable=disabled,
                    logout=True,
                    user_id=user_id,
                )
                db.session.add(user)
                db.session.commit()
            except:
                raise DataInjectionError
            finally:
                db.session.close()
    except DatabaseErrors:
        raise
    except Exception:
        raise DatabaseConnectionError
