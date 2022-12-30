from src.common.utils.constants import DB_CONNECTION_LINK
from src.db.database import Therapist, Vent
from src.db.errors import DataInjectionError, DatabaseErrors, DatabaseConnectionError, ItemNotFound
from src.db.utils import DBConnection


def add_vent(id, text):
    with DBConnection(DB_CONNECTION_LINK, False) as db:
        vent = Vent(
            v_id=id,
            # v_picture=picture,
            v_text=text,
        )
        db.session.add(vent)
        db.session.commit()
        db.session.close()
        return id


def get_vents():
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                data = (
                    db.session.querry(Vent).all()
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
                db.session.close()
    except DatabaseErrors:
        raise
    except Exception:
        raise DatabaseConnectionError
