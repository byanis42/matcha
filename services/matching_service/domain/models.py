# services/matching_service/domain/models.py

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Optionnel: si vous décidez de stocker un "MatchingHistory" localement,
# vous pourriez définir ici une table. Ex:

# from sqlalchemy import Column, Integer, String, DateTime, Float
# from datetime import datetime

# class MatchingHistory(Base):
#     __tablename__ = "matching_history"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, nullable=False)
#     candidate_user_id = Column(Integer, nullable=False)
#     score = Column(Float, default=0.0)
#     matched_at = Column(DateTime, default=datetime.utcnow)
