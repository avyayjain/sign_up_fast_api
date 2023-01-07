from sqlalchemy import (
    Column,
    String, Integer,
    BIGINT
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = "user_info"

    email_id = Column(String, primary_key=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Therapist(Base):
    __tablename__ = "therapist_info"

    t_name = Column(String, primary_key=True, nullable=False)
    t_city = Column(String, nullable=False)
    t_address = Column(String, nullable=False)
    t_dis = Column(String, nullable=False)
    t_services = Column(String, nullable=False)
    t_phone = Column(BIGINT, nullable=True)
    t_picture = Column(String, nullable=True)
    t_spec = Column(String, nullable=False)


class Vent(Base):
    __tablename__ = "anonymous_vent"

    v_id = Column(Integer, primary_key=True, nullable=False)
    v_picture = Column(String, nullable=True)
    v_text = Column(String, nullable=True)
