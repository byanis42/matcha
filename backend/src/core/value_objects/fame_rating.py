from pydantic import BaseModel, field_validator
from enum import Enum


class FameLevel(Enum):
    NEWCOMER = "newcomer"
    RISING = "rising"
    POPULAR = "popular"
    FAMOUS = "famous"
    LEGENDARY = "legendary"


class FameRating(BaseModel):
    value: float
    
    def __init__(self, value: float):
        super().__init__(value=value)
    
    @field_validator('value')
    @classmethod
    def validate_rating(cls, v):
        if not 0.0 <= v <= 5.0:
            raise ValueError('Fame rating must be between 0.0 and 5.0')
        return round(v, 2)
    
    def __str__(self) -> str:
        return f"{self.value:.2f}"
    
    def __float__(self) -> float:
        return self.value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, FameRating):
            return self.value == other.value
        if isinstance(other, (int, float)):
            return self.value == other
        return False
    
    def __lt__(self, other) -> bool:
        if isinstance(other, FameRating):
            return self.value < other.value
        if isinstance(other, (int, float)):
            return self.value < other
        return False
    
    def __le__(self, other) -> bool:
        return self < other or self == other
    
    def __gt__(self, other) -> bool:
        return not self <= other
    
    def __ge__(self, other) -> bool:
        return not self < other
    
    @property
    def level(self) -> FameLevel:
        if self.value < 1.0:
            return FameLevel.NEWCOMER
        elif self.value < 2.0:
            return FameLevel.RISING
        elif self.value < 3.5:
            return FameLevel.POPULAR
        elif self.value < 4.5:
            return FameLevel.FAMOUS
        else:
            return FameLevel.LEGENDARY
    
    def increase(self, amount: float) -> 'FameRating':
        new_value = min(5.0, self.value + amount)
        return FameRating(new_value)
    
    def decrease(self, amount: float) -> 'FameRating':
        new_value = max(0.0, self.value - amount)
        return FameRating(new_value)