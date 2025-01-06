# services/chat_service/tests/conftest.py
import pytest
from services.chat_service.domain.models import ChatMessage
from services.chat_service.infrastructure.database import get_session

@pytest.fixture(scope="function", autouse=True)
def clean_db():
    """
    Supprime toutes les entrées de chat_messages avant chaque test.
    """
    with get_session() as db:
        db.query(ChatMessage).delete()
        db.commit()
    yield
    # Optionnel : on pourrait re-supprimer après si besoin
