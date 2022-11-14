from sqlalchemy import (
    Boolean,
    Column,
    String,
)

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Users(Base):
    __tablename__ = "user_info"

    email_id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    disable = Column(Boolean, nullable=False)
    logout = Column(Boolean, nullable=False)
    user_id = Column(String, nullable=False, unique=True)
