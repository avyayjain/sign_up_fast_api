from src.common.utils.constants import DB_CONNECTION_LINK
from src.db.errors import (
    ItemNotFound,
    DatabaseErrors,
    DataExtractionError,
    DatabaseConnectionError,
)
from src.db.utils import DBConnection
from src.db.database import Users


def delete_user(user_email):
    """

    @param user_email: User Email
    @type user_email: str
    @rtype: None
    """
    try:
        with DBConnection( False) as db:
            try:
                data = (
                    db.query(Users).filter(Users.email_id == user_email).first()
                )
                if not data:
                    raise ItemNotFound
                db.delete(data)
                db.commit()
            except DatabaseErrors:
                raise
            except Exception:
                raise DataExtractionError
            finally:
                db.close()
    except DatabaseErrors:
        raise
    except Exception:
        raise DatabaseConnectionError
