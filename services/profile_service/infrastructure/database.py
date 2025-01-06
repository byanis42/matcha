# services/profile_service/infrastructure/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from services.profile_service.domain.models import Base
# On suppose que vous avez un module 'settings'
from services.profile_service.application.settings import settings

engine = create_engine(
    settings.database_url,
    echo=False
)

def init_db():
    """Crée les tables si elles n'existent pas déjà (usage dev/test)."""
    Base.metadata.create_all(bind=engine)

def get_session():
    """Context manager pour récupérer une session SQLAlchemy."""
    with Session(engine) as session:
        yield session
