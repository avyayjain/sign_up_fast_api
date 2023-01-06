from src.common.utils.constants import DB_CONNECTION_LINK
from src.db.database import Therapist, Vent
from src.db.errors import DataInjectionError, DatabaseErrors, DatabaseConnectionError, ItemNotFound
from src.db.utils import DBConnection


def add_vent(id, text,picture):
    with DBConnection( False) as db:
        vent = Vent(
            v_id=id,
            v_picture=picture,
            v_text=text,
        )
        db.add(vent)
        db.commit()
        db.close()
        return id


def get_vents():
    try:
        with DBConnection( False) as db:
            try:
                data = (
                    db.query(Vent).all()
                )
                if not data:
                    raise ItemNotFound
                response = []
                for data in data:
                    vent = {
                        "id": data.v_id,
                        "text": data.v_text,
                    }
                    response.append(vent)

                return response
            except:
                raise DataInjectionError
            finally:
                db.close()
    except DatabaseErrors:
        raise
    except Exception:
        raise DatabaseConnectionError
