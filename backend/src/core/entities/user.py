from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator

from ..value_objects.age import Age
from ..value_objects.email import Email
from ..value_objects.fame_rating import FameRating
from ..value_objects.location import Location


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"
    PENDING_VERIFICATION = "pending_verification"


class User(BaseModel):
    model_config = ConfigDict(use_enum_values=True, arbitrary_types_allowed=True)

    id: int | None = None
    username: str
    email: Email
    password_hash: str
    first_name: str
    last_name: str
    status: UserStatus = UserStatus.PENDING_VERIFICATION
    email_verified: bool = False
    last_seen: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not v or len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(v) > 50:
            raise ValueError("Username cannot exceed 50 characters")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, v):
        if not v or len(v) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if len(v) > 50:
            raise ValueError("Name cannot exceed 50 characters")
        return v

    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE

    def is_verified(self) -> bool:
        return self.email_verified

    def verify_email(self) -> None:
        self.email_verified = True
        if self.status == UserStatus.PENDING_VERIFICATION:
            self.status = UserStatus.ACTIVE

    def deactivate(self) -> None:
        self.status = UserStatus.INACTIVE

    def ban(self) -> None:
        self.status = UserStatus.BANNED

    def update_last_seen(self) -> None:
        self.last_seen = datetime.utcnow()

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def can_be_matched(self) -> bool:
        return self.is_active() and self.is_verified()


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non_binary"
    OTHER = "other"


class SexualPreference(str, Enum):
    HETEROSEXUAL = "heterosexual"
    HOMOSEXUAL = "homosexual"
    BISEXUAL = "bisexual"
    PANSEXUAL = "pansexual"
    ASEXUAL = "asexual"


class UserProfile(BaseModel):
    model_config = ConfigDict(use_enum_values=True, arbitrary_types_allowed=True)

    id: int | None = None
    user_id: int
    age: Age
    gender: Gender
    sexual_preference: SexualPreference
    biography: str
    location: Location | None = None
    fame_rating: FameRating = FameRating(0.0)
    interests: list[str] = []
    pictures: list[str] = []
    profile_completed: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_validator("biography")
    @classmethod
    def validate_biography(cls, v):
        if len(v) > 500:
            raise ValueError("Biography cannot exceed 500 characters")
        return v

    @field_validator("interests")
    @classmethod
    def validate_interests(cls, v):
        if len(v) > 10:
            raise ValueError("Cannot have more than 10 interests")
        return v

    @field_validator("pictures")
    @classmethod
    def validate_pictures(cls, v):
        if len(v) > 5:
            raise ValueError("Cannot have more than 5 pictures")
        return v

    def add_interest(self, interest: str) -> None:
        if interest not in self.interests and len(self.interests) < 10:
            self.interests.append(interest)

    def remove_interest(self, interest: str) -> None:
        if interest in self.interests:
            self.interests.remove(interest)

    def add_picture(self, picture_url: str) -> None:
        if len(self.pictures) < 5:
            self.pictures.append(picture_url)

    def remove_picture(self, picture_url: str) -> None:
        if picture_url in self.pictures:
            self.pictures.remove(picture_url)

    def is_complete(self) -> bool:
        return (
            self.age is not None
            and self.gender is not None
            and self.sexual_preference is not None
            and self.biography
            and self.location is not None
            and len(self.pictures) >= 1
        )

    def update_fame_rating(self, new_rating: float) -> None:
        self.fame_rating = FameRating(new_rating)

    def matches_preference(self, other_gender: Gender) -> bool:
        if self.sexual_preference == SexualPreference.HETEROSEXUAL:
            return (self.gender == Gender.MALE and other_gender == Gender.FEMALE) or (
                self.gender == Gender.FEMALE and other_gender == Gender.MALE
            )
        elif self.sexual_preference == SexualPreference.HOMOSEXUAL:
            return self.gender == other_gender
        elif self.sexual_preference in [
            SexualPreference.BISEXUAL,
            SexualPreference.PANSEXUAL,
        ]:
            return True
        return False
