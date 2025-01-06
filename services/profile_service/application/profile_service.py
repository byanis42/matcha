# services/profile_service/application/profile_service.py

from sqlalchemy.orm import Session
from services.profile_service.domain.models import Profile

def create_profile(db: Session, user_id: int, gender: str, orientation: str, biography: str, interests: str, pictures: str):
    """
    Crée un nouveau profil pour l'utilisateur 'user_id'.
    On suppose que l'utilisateur n'a pas encore de profil dans la table 'profiles'.
    """
    existing = db.query(Profile).filter(Profile.user_id == user_id).first()
    if existing:
        # On peut lever une exception ou retourner None
        raise ValueError("Profile already exists for this user_id.")

    profile = Profile(
        user_id=user_id,
        gender=gender,
        orientation=orientation,
        biography=biography,
        interests=interests,
        pictures=pictures
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def get_profile(db: Session, user_id: int):
    """
    Récupère un profil par user_id. Retourne None si pas trouvé.
    """
    return db.query(Profile).filter(Profile.user_id == user_id).one_or_none()

def update_profile(db: Session, user_id: int, gender: str = None, orientation: str = None,
                   biography: str = None, interests: str = None):
    """
    Met à jour les champs d'un profil existant. Tout paramètre non fourni reste inchangé.
    """
    profile = db.query(Profile).filter(Profile.user_id == user_id).one_or_none()
    if not profile:
        raise ValueError("Profile not found.")

    if gender is not None:
        profile.gender = gender
    if orientation is not None:
        profile.orientation = orientation
    if biography is not None:
        profile.biography = biography
    if interests is not None:
        profile.interests = interests

    db.commit()
    db.refresh(profile)
    return profile

def update_pictures(db: Session, user_id: int, pictures: str):
    """
    Met à jour la liste des URLs de photo (séparées par des virgules).
    On vérifie qu'il n'y ait pas plus de 5 URLs.
    """
    profile = db.query(Profile).filter(Profile.user_id == user_id).one_or_none()
    if not profile:
        raise ValueError("Profile not found.")

    urls = [url.strip() for url in pictures.split(",") if url.strip()]
    if len(urls) > 5:
        raise ValueError("Cannot have more than 5 pictures.")

    profile.pictures = ",".join(urls)

    db.commit()
    db.refresh(profile)
    return profile
