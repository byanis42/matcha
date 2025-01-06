# services/chat_service/infrastructure/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from services.chat_service.domain.models import Base
from services.chat_service.application.settings import settings

engine = create_engine(settings.database_url, echo=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    with Session(engine) as session:
        yield session
