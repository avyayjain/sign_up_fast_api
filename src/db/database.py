from sqlalchemy import (
    Boolean,
    Column,
    String, Integer,
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


class Therapist(Base):
    __tablename__ = "therapist_info"

    t_name = Column(String, primary_key=True, nullable=False)
    t_city = Column(String, nullable=False)
    t_phone = Column(Integer, nullable=True)
    t_email = Column(String, nullable=True)


class Vent(Base):
    __tablename__ = "anonymous_vent"

    v_id = Column(String, primary_key=True, nullable=False)
    # v_picture = Column(String, nullable=False)
    v_text = Column(Integer, nullable=True)
