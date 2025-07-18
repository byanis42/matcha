from datetime import date, datetime

from pydantic import BaseModel, field_validator


class Age(BaseModel):
    value: int

    def __init__(self, value: int | date | datetime):
        if isinstance(value, date | datetime):
            today = date.today()
            birth_date = value.date() if isinstance(value, datetime) else value
            age_value = (
                today.year
                - birth_date.year
                - ((today.month, today.day) < (birth_date.month, birth_date.day))
            )
        else:
            age_value = value

        super().__init__(value=age_value)

    @field_validator("value")
    @classmethod
    def validate_age(cls, v):
        if not 18 <= v <= 120:
            raise ValueError("Age must be between 18 and 120")
        return v

    def __str__(self) -> str:
        return str(self.value)

    def __int__(self) -> int:
        return self.value

    def __eq__(self, other) -> bool:
        if isinstance(other, Age):
            return self.value == other.value
        if isinstance(other, int):
            return self.value == other
        return False

    def __lt__(self, other) -> bool:
        if isinstance(other, Age):
            return self.value < other.value
        if isinstance(other, int):
            return self.value < other
        return False

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return not self < other

    def is_adult(self) -> bool:
        return self.value >= 18

    def is_senior(self) -> bool:
        return self.value >= 65
