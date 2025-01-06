# services/profile_service/domain/models.py

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from datetime import datetime

class Base(DeclarativeBase):
    """Base Declarative pour SQLAlchemy 2.0."""
    pass

class Profile(Base):
    """
    Profil d'un utilisateur.
    Couvre les besoins du chapitre IV.2 : genre, orientation, biographie,
    intérêts (tags), photos (jusqu’à 5), etc.
    Inclut :
    - fame_rating
    - localisation GPS (latitude/longitude)
    - last_connection pour savoir si un user est online/récemment connecté
    """
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)

    gender = Column(String, nullable=True)       # 'M', 'F', 'O', etc.
    orientation = Column(String, nullable=True)  # 'hetero', 'bi', 'homo'...
    biography = Column(Text, nullable=True)

    # Ex: "#vegan,#geek,#piercing" => on pourra séparer par virgules, ou JSON
    interests = Column(Text, nullable=True)

    # Jusqu'à 5 photos => on stocke en CSV : "url1,url2,url3"
    pictures = Column(Text, nullable=True)

    fame_rating = Column(Float, default=0.0)
    gps_lat = Column(Float, nullable=True)   # localisation lat
    gps_long = Column(Float, nullable=True)  # localisation long

    # Pour gérer "qui est en ligne ?"
    last_connection = Column(DateTime, nullable=True)

class VisitHistory(Base):
    """
    Permet de stocker qui a visité le profil de qui,
    pour que l'utilisateur sache qui l'a vu (IV.2: "The user must be able to check who has viewed their profile").
    """
    __tablename__ = "visit_history"

    id = Column(Integer, primary_key=True)
    viewer_id = Column(Integer, nullable=False)  # qui visite
    viewed_id = Column(Integer, nullable=False)  # profil visité
    timestamp = Column(DateTime, default=datetime.utcnow)

    # On peut ajouter un index pour accélérer les requêtes
    # e.g. UniqueConstraint('viewer_id', 'viewed_id', name='uix_viewer_viewed')

class Like(Base):
    """
    Gère le fait qu'un user A "like" (montre un intérêt) pour un user B.
    - IV.5: "Like" -> connect => chat possible
    """
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)       # qui like
    target_user_id = Column(Integer, nullable=False) # qui est liké
    timestamp = Column(DateTime, default=datetime.utcnow)

    # ex. UniqueConstraint pour éviter les doublons
    __table_args__ = (
        UniqueConstraint('user_id', 'target_user_id', name='uix_user_like_once'),
    )

class Block(Base):
    """
    Gère le blocage d'un user B par un user A.
    - IV.5: "Block a user. A blocked user won't appear in search results..."
    """
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)         # qui bloque
    blocked_user_id = Column(Integer, nullable=False) # qui est bloqué
    timestamp = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('user_id', 'blocked_user_id', name='uix_user_block_once'),
    )

class FakeReport(Base):
    """
    Permet de signaler un user comme 'fake account'.
    (IV.5: "Report a user as a 'fake account'").
    """
    __tablename__ = "fake_reports"

    id = Column(Integer, primary_key=True)
    reporter_id = Column(Integer, nullable=False)     # qui signale
    reported_user_id = Column(Integer, nullable=False)# qui est signalé
    timestamp = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('reporter_id', 'reported_user_id', name='uix_user_report_once'),
    )
