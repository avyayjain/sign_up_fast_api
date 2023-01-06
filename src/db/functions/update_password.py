from src.common.utils.constants import DB_CONNECTION_LINK
from src.common.utils.pwd_helper import get_password_hash
from src.db.database import Users
from src.db.errors import (
    DataInjectionError,
    DatabaseErrors,
    DatabaseConnectionError,
    ItemNotFound,
)
from src.db.utils import DBConnection


def update_pass(user_email: str, password: str):
    """

    :param user_email: User Email
    :param password: User Password
    :return: None
    """
    try:
        with DBConnection( False) as db:
            try:
                data = (
                    db.query(Users).filter(Users.email_id == user_email).first()
                )
                if not data:
                    raise ItemNotFound
                data.hashed_password = get_password_hash(password)
                db.commit()
            except:
                raise DataInjectionError
            finally:
                db.close()
    except DatabaseErrors:
        raise
    except Exception:
        raise DatabaseConnectionError