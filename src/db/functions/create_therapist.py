from src.common.utils.constants import DB_CONNECTION_LINK
from src.common.utils.pwd_helper import get_password_hash
from src.db.database import Users, Therapist
from src.db.errors import DataInjectionError, DatabaseErrors, DatabaseConnectionError
from src.db.utils import DBConnection


def create_user(t_name: str, t_city: str, t_phone: int, t_email=str):

    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                therapist = Therapist(
                    t_name=t_name,
                    t_city=t_city,
                    t_email=t_email,
                    t_phone=t_phone,
                )
                db.session.add(therapist)
                db.session.commit()
            except:
                raise DataInjectionError
            finally:
                db.session.close()
    except DatabaseErrors:
        raise
    except Exception:
        raise DatabaseConnectionError