# services/auth_service/interface/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

# Import de la session + init_db
from services.auth_service.infrastructure.database import get_session, init_db
# Import des fonctions d'auth
from services.auth_service.application.auth_service import (
    get_password_hash, create_access_token, authenticate_user
)
# Import du modèle User pour manipuler la table
from services.auth_service.domain.models import User

# Settings + CORS
from services.auth_service.application.settings import settings
from fastapi.middleware.cors import CORSMiddleware

# Crée l'application FastAPI
app = FastAPI()

# Créer les tables une bonne fois (dev/test) :
init_db()

# Configuration CORS (adapte si besoin)
origins = [
    "http://localhost:3000",
    "https://localhost:8443",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models pour nos endpoints
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Endpoint /register
@app.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_session)):
    # Vérifie si l'email ou le username existe déjà
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")

    hashed_password = get_password_hash(user.password)

    new_user = User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint /login
@app.post("/login", response_model=Token)
def login(form_data: UserLogin, db: Session = Depends(get_session)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
