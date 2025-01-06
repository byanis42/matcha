# services/matching_service/interface/main.py

from fastapi import FastAPI, Query
from services.matching_service.application.matching_service import (
    get_suggestions_for_user,
    get_swipe_deck_for_user
)
from services.matching_service.infrastructure.database import init_db

app = FastAPI()

# init_db() # si on veut créer d'éventuelles tables locales

@app.get("/suggestions")
def get_suggestions(user_id: int = Query(...)):
    """
    Renvoie un top 20 suggestions (triées) pour user_id.
    """
    suggestions = get_suggestions_for_user(user_id)
    return suggestions

@app.get("/swipe/deck")
def get_swipe_deck(user_id: int = Query(...), batch_size: int = Query(10)):
    """
    Renvoie un 'deck' (liste) de size = batch_size,
    ordonné, pour la logique Tinder-like.
    """
    deck = get_swipe_deck_for_user(user_id, batch_size)
    return deck
