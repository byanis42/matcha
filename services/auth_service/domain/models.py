# services/auth_service/domain/models.py

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean

# DeclarativeBase est la nouvelle API "2.0" pour définir la base déclarative
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
