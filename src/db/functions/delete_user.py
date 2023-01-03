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
                    db.session.query(Users).filter(Users.email_id == user_email).first()
                )
                if not data:
                    raise ItemNotFound
                db.session.delete(data)
                db.session.commit()
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
