# services/notification_service/infrastructure/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from services.notification_service.domain.models import Base

# Supposez un 'settings.py' ou un os.getenv("DATABASE_URL")
from services.notification_service.application.settings import settings

engine = create_engine(settings.database_url, echo=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    with Session(engine) as session:
        yield session
