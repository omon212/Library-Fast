from enum import Enum
from sqlalchemy import Integer, String, Column
from app.databace import Base


class UserRole(str, Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    OPERATOR = 'OPERATOR'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
