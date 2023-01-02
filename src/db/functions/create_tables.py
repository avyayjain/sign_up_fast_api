from sqlalchemy import create_engine
from src.common.utils.constants import DB_CONNECTION_LINK
from src.db.errors import DatabaseErrors, DatabaseConnectionError
from src.db.database import Base


def create_tables():
    try:
        eng = create_engine(url=DB_CONNECTION_LINK)
        print("successfully")
    except:
        raise DatabaseConnectionError
    try:
        Base.metadata.create_all(eng)
        print("successfully")
    except:
        raise DatabaseErrors
