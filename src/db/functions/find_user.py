from src.common.utils.constants import DB_CONNECTION_LINK
from src.db.errors import (
    ItemNotFound,
    DatabaseErrors,
    DataExtractionError,
    DatabaseConnectionError,
)
from src.db.utils import DBConnection
from src.db.database import Users


def find_user_pass(user_email):
    """

    @param user_email: User Email
    @type user_email: str
    @return: hashed password and data disable
    @rtype: Tuple[str,bool]
    """
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                data = (
                    db.session.query(Users).filter(Users.email_id == user_email).first()
                )
                if not data:
                    raise ItemNotFound
                if data.hashed_password:
                    hash_pass = data.hashed_password
                    disable_status = data.disable
                    logout = data.logout
                    user_id = data.user_id
                    return hash_pass, disable_status, logout, user_id
                else:
                    raise DataExtractionError
            except DatabaseErrors:
                raise
            except Exception:
                raise DataExtractionError
            finally:
                db.session.close()
    except DatabaseErrors:
        raise
    except Exception:
        raise DatabaseConnectionError
