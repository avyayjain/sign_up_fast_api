from src.common.utils.constants import DB_CONNECTION_LINK
from src.db.database import Therapist
from src.db.errors import DataInjectionError, DatabaseErrors, DatabaseConnectionError, ItemNotFound
from src.db.utils import DBConnection


def therapist_info(t_name: str, t_city: str, t_phone: int, t_address: str, t_dis: str, t_services: str,
                   t_picture: str, t_spec: str):
    try:
        with DBConnection(False) as db:
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
                db.add(therapist)
                db.commit()
            except:
                raise DataInjectionError
            finally:
                db.close()
    except DatabaseErrors:
        raise
    except Exception:
        raise DatabaseConnectionError


def get_therapist_info():
    try:
        with DBConnection(False) as session:
            try:
                data = (
                    session.query(Therapist).all()
                )
                if not data:
                    raise ItemNotFound
                response = []
                for data in data:
                    therapist = {
                        "name": data.t_name,
                        "city": data.t_city,
                        "phone": data.t_phone,
                        "description": data.t_dis,
                        "services": data.t_services,
                        "picture": data.t_picture,
                        "specialization": data.t_spec,
                        "address": data.t_address,
                    }
                    response.append(therapist)

                return response
            except:
                raise DataInjectionError

    except DatabaseErrors:
        raise
    except Exception:
        raise DatabaseConnectionError
