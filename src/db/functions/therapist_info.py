from src.common.utils.constants import DB_CONNECTION_LINK
from src.db.database import Therapist
from src.db.errors import DataInjectionError, DatabaseErrors, DatabaseConnectionError, ItemNotFound
from src.db.utils import DBConnection


def therapist_info(t_name: str, t_city: str, t_phone: int, t_address: str, t_dis: str, t_services: str,
                   t_picture: str, t_spec: str):
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                therapist = Therapist(
                    t_name=t_name,
                    t_city=t_city,
                    t_phone=t_phone,
                    t_picture=t_picture,
                    t_address=t_address,
                    t_dis=t_dis,
                    t_services=t_services,
                    t_spec=t_spec
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
