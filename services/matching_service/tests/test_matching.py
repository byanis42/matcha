# services/matching_service/tests/test_matching.py

import pytest
from fastapi.testclient import TestClient
from services.matching_service.interface.main import app

client = TestClient(app)

def mock_fetch_user_profile(user_id):
    """
    On suppose que user_id=1234 => M, hetero
    """
    return {
        "user_id": user_id,
        "gender": "M",
        "orientation": "hetero",  # orientation courante
        "interests": "#vegan,#geek",
        "gps_lat": 0.0,
        "gps_long": 0.0,
        "fame_rating": 2.0
    }

def mock_fetch_all_profiles():
    return [
        {
            "user_id": 9999,
            "gender": "F",
            "orientation": "hetero",
            "interests": "#vegan,#sport",
            "gps_lat": 0.1,
            "gps_long": 0.1,
            "fame_rating": 5.0
        },
        {
            # user qui a un orientation = 'bi' =>
            # => il aime tout,
            # => mais
            "user_id": 8888,
            "gender": "M",
            "orientation": "homo",
            "interests": "#geek,#food",
            "gps_lat": 10.0,
            "gps_long": 10.0,
            "fame_rating": 1.0
        }
    ]

def mock_fetch_likers_for_user(user_id):
    return [9999]  # On suppose que 9999 a déjà liké user_id => bonus

@pytest.fixture
def patch_fetch(mocker):
    mocker.patch("services.matching_service.application.matching_service.fetch_user_profile", side_effect=mock_fetch_user_profile)
    mocker.patch("services.matching_service.application.matching_service.fetch_all_profiles", side_effect=mock_fetch_all_profiles)
    mocker.patch("services.matching_service.application.matching_service.fetch_likers_for_user", side_effect=mock_fetch_likers_for_user)

def test_get_suggestions(patch_fetch):
    # user_id=1234 => M, hetero
    resp = client.get("/suggestions?user_id=1234")
    assert resp.status_code == 200
    data = resp.json()
    # Sur 2 profils,
    # - 9999 => F, hetero => réciproque OK => on l'a
    # - 8888 => M, homo => pas compatible => n'apparait pas
    # => total 1
    assert len(data) == 1
    # 9999 est présent
    assert data[0]["user_id"] == 9999

def test_get_swipe_deck(patch_fetch):
    # On vérifie qu'on a un deck de 1
    resp = client.get("/swipe/deck?user_id=1234&batch_size=10")
    assert resp.status_code == 200
    deck = resp.json()
    # On s'attend à 1 profil => 9999
    assert len(deck) == 1
    assert deck[0]["user_id"] == 9999
