# services/auth_service/tests/conftest.py
import pytest
from sqlalchemy.orm import Session

from services.auth_service.infrastructure.database import engine, get_session, Base
from services.auth_service.domain.models import User

@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    """
    Crée les tables une seule fois pour l'ensemble de la session de tests.
    Si vous préférez les recréer entre chaque test, vous pouvez mettre scope="function".
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # (optionnel) nettoyer les tables après tous les tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """
    Fournit une session de base de données pour chaque test.
    """
    with get_session() as session:
        yield session
