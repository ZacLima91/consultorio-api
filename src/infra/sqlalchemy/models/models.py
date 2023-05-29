from sqlalchemy import Column, Integer, String, ARRAY, Boolean
from src.infra.sqlalchemy.config.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    cpf = Column(String)
    password = Column(String)
    laudos = Column(ARRAY(String))
    role = Column(Boolean)
