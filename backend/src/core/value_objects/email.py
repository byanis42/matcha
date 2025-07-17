from pydantic import BaseModel, EmailStr, field_validator
import re


class Email(BaseModel):
    value: EmailStr
    
    def __init__(self, value: str):
        super().__init__(value=value)
    
    @field_validator('value')
    @classmethod
    def validate_email(cls, v):
        if not v:
            raise ValueError('Email cannot be empty')
        return v
    
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Email):
            return self.value == other.value
        return False
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    @property
    def domain(self) -> str:
        return self.value.split('@')[1]
    
    @property
    def local_part(self) -> str:
        return self.value.split('@')[0]