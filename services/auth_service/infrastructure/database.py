# services/auth_service/infrastructure/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# On importe le 'Base' depuis models.py
from services.auth_service.domain.models import Base
# On importe tes settings depuis 'services.auth_service.application.settings'
from services.auth_service.application.settings import settings

# Crée l'engine : style synchrone, pas d'async ici
engine = create_engine(
    settings.database_url,
    echo=False  # Passe à True si tu veux afficher les requêtes SQL dans les logs
)

def init_db():
    """Créer les tables si elles n'existent pas (utilisé pour dev/test)."""
    Base.metadata.create_all(bind=engine)

def get_session():
    """
    Fournit une session synchrone via un context manager,
    utile pour FastAPI (ou usage direct).
    """
    with Session(engine) as session:
        yield session
