# services/profile_service/interface/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from services.profile_service.infrastructure.database import init_db, get_session
from services.profile_service.application.profile_service import (
    create_profile, get_profile, update_profile, update_pictures
)
from services.profile_service.application.settings import settings
from pydantic import BaseModel

app = FastAPI()

# Créer les tables au démarrage (dev/test)
init_db()


# ---- Schémas Pydantic pour les endpoints ----
class ProfileCreateSchema(BaseModel):
    user_id: int
    gender: str
    orientation: str
    biography: str
    interests: str
    pictures: str = ""  # liste de photos, ex. "url1,url2"

class ProfileUpdateSchema(BaseModel):
    gender: str | None = None
    orientation: str | None = None
    biography: str | None = None
    interests: str | None = None

class PicturesUpdateSchema(BaseModel):
    pictures: str

class ProfileOutSchema(BaseModel):
    user_id: int
    gender: str | None
    orientation: str | None
    biography: str | None
    interests: str | None
    pictures: str | None

    class Config:
        orm_mode = True


# ---- Endpoints ----

@app.post("/profiles", response_model=ProfileOutSchema)
def create_profile_endpoint(data: ProfileCreateSchema, db: Session = Depends(get_session)):
    try:
        profile = create_profile(
            db=db,
            user_id=data.user_id,
            gender=data.gender,
            orientation=data.orientation,
            biography=data.biography,
            interests=data.interests,
            pictures=data.pictures
        )
        return profile
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/profiles/{user_id}", response_model=ProfileOutSchema)
def get_profile_endpoint(user_id: int, db: Session = Depends(get_session)):
    profile = get_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
    return profile

@app.put("/profiles/{user_id}", response_model=ProfileOutSchema)
def update_profile_endpoint(user_id: int, data: ProfileUpdateSchema, db: Session = Depends(get_session)):
    try:
        profile = update_profile(
            db=db,
            user_id=user_id,
            gender=data.gender,
            orientation=data.orientation,
            biography=data.biography,
            interests=data.interests
        )
        return profile
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/profiles/{user_id}/pictures", response_model=ProfileOutSchema)
def update_pictures_endpoint(user_id: int, data: PicturesUpdateSchema, db: Session = Depends(get_session)):
    try:
        profile = update_pictures(db, user_id, data.pictures)
        return profile
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
