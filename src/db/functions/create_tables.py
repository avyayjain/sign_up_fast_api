from sqlalchemy import create_engine
from src.common.utils.constants import DB_CONNECTION_LINK
import src.db.database as db
from src.db.errors import DatabaseErrors, DatabaseConnectionError


def create_tables():
    try:
        eng = create_engine(DB_CONNECTION_LINK)
    except:
        raise DatabaseConnectionError
    try:
        db.Users.metadata.create_all(eng)
    except:
        raise DatabaseErrors