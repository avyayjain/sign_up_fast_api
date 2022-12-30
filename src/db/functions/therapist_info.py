from src.common.utils.constants import DB_CONNECTION_LINK
from src.db.database import Therapist
from src.db.errors import DataInjectionError, DatabaseErrors, DatabaseConnectionError, ItemNotFound
from src.db.utils import DBConnection


def therapist_info(name, city, email, phone):
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                therapist = Therapist(
                    t_name=name,
                    t_city=city,
                    t_email=email,
                    t_phone=phone,
                )
                db.session.add(therapist)
                db.session.commit()
                return name
            except:
                raise DataInjectionError
            finally:
                db.session.close()
    except DatabaseErrors:
        raise
    except Exception:
        raise DatabaseConnectionError


def get_therapist_info():
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                data = (
                    db.session.querry(Therapist).all()
                )
                if not data:
                    raise ItemNotFound
                response = []
                for data in data:
                    therapist = {
                        "name": data.t_name,
                        "city": data.t_city,
                        "phone": data.t_phone,
                        "email": data.t_email
                    }
                    response.append(therapist)

                return response
            except:
                raise DataInjectionError
            finally:
                db.session.close()
    except DatabaseErrors:
        raise
    except Exception:
        raise DatabaseConnectionError
