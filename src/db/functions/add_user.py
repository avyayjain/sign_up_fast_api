from src.db.database import Users
from src.db.errors import DataInjectionError, DatabaseErrors, DatabaseConnectionError
from src.db.utils import DBConnection


def create_user(user_name: str, user_email: str, password: str):
    """


    :param user_name:
    :param user_email: User Email
    :param password: User Password
    :return: None
    """
    try:
        with DBConnection(False) as db:
            try:
                user = Users(
                    name=user_name,
                    email_id=user_email,
                    hashed_password=password,

                )
                db.session.add(user)
                db.session.commit()
            except Exception:
                raise DataInjectionError
            finally:
                db.session.close()
    except DatabaseErrors:
        raise
    except Exception:
        raise DatabaseConnectionError
