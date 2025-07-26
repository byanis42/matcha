from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.core.entities.user import Gender, SexualPreference, UserProfile
from src.core.value_objects.location import Location


class ProfileCreateRequest(BaseModel):
    """Request schema for creating a user profile."""

    age: int = Field(..., ge=18, le=100, description="User age (18-100)")
    gender: Gender = Field(..., description="User gender")
    sexual_preference: SexualPreference = Field(..., description="Sexual preference")
    biography: str = Field(
        ..., min_length=10, max_length=500, description="User biography"
    )
    latitude: float | None = Field(
        None, ge=-90, le=90, description="Latitude coordinate"
    )
    longitude: float | None = Field(
        None, ge=-180, le=180, description="Longitude coordinate"
    )
    city: str | None = Field(None, max_length=100, description="City name")
    country: str | None = Field(None, max_length=100, description="Country name")
    interests: list[str] | None = Field(
        None, max_length=10, description="List of interests (max 10)"
    )

    @field_validator("interests")
    @classmethod
    def validate_interests(cls, v):
        if v is not None and len(v) > 10:
            raise ValueError("Cannot have more than 10 interests")
        return v

    @field_validator("biography")
    @classmethod
    def validate_biography(cls, v):
        stripped = v.strip()
        if not stripped:
            raise ValueError("Biography cannot be empty")
        if len(stripped) < 10:
            raise ValueError("Biography must be at least 10 characters long")
        return stripped


class ProfileUpdateRequest(BaseModel):
    """Request schema for updating a user profile."""

    age: int | None = Field(None, ge=18, le=100, description="User age (18-100)")
    gender: Gender | None = Field(None, description="User gender")
    sexual_preference: SexualPreference | None = Field(
        None, description="Sexual preference"
    )
    biography: str | None = Field(
        None, min_length=10, max_length=500, description="User biography"
    )
    latitude: float | None = Field(
        None, ge=-90, le=90, description="Latitude coordinate"
    )
    longitude: float | None = Field(
        None, ge=-180, le=180, description="Longitude coordinate"
    )
    city: str | None = Field(None, max_length=100, description="City name")
    country: str | None = Field(None, max_length=100, description="Country name")
    interests: list[str] | None = Field(
        None, max_length=10, description="List of interests (max 10)"
    )

    @field_validator("interests")
    @classmethod
    def validate_interests(cls, v):
        if v is not None and len(v) > 10:
            raise ValueError("Cannot have more than 10 interests")
        return v

    @field_validator("biography")
    @classmethod
    def validate_biography(cls, v):
        if v is not None:
            stripped = v.strip()
            if not stripped:
                raise ValueError("Biography cannot be empty")
            if len(stripped) < 10:
                raise ValueError("Biography must be at least 10 characters long")
            return stripped
        return v


class LocationResponse(BaseModel):
    """Response schema for location data."""

    latitude: float
    longitude: float
    city: str | None
    country: str | None

    @classmethod
    def from_value_object(cls, location: Location) -> "LocationResponse":
        return cls(
            latitude=location.latitude,
            longitude=location.longitude,
            city=location.city,
            country=location.country,
        )


class ProfileResponse(BaseModel):
    """Response schema for user profile."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    age: int
    gender: Gender
    sexual_preference: SexualPreference
    biography: str
    location: LocationResponse | None
    fame_rating: float
    interests: list[str]
    pictures: list[str]
    profile_completed: bool
    created_at: datetime | None
    updated_at: datetime | None

    @classmethod
    def from_entity(cls, profile: UserProfile) -> "ProfileResponse":
        """Create response from domain entity."""
        location_response = None
        if profile.location:
            location_response = LocationResponse.from_value_object(profile.location)

        return cls(
            id=profile.id,
            user_id=profile.user_id,
            age=profile.age.value,
            gender=profile.gender,
            sexual_preference=profile.sexual_preference,
            biography=profile.biography,
            location=location_response,
            fame_rating=profile.fame_rating.value,
            interests=profile.interests,
            pictures=profile.pictures,
            profile_completed=profile.profile_completed,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        )


class ImageUploadResponse(BaseModel):
    """Response schema for image upload."""

    image_url: str = Field(..., description="URL of the uploaded image")


class ImageReorderRequest(BaseModel):
    """Request schema for reordering profile images."""

    image_urls: list[str] = Field(
        ..., min_length=1, max_length=5, description="Ordered list of image URLs"
    )

    @field_validator("image_urls")
    @classmethod
    def validate_image_urls(cls, v):
        if len(set(v)) != len(v):
            raise ValueError("Image URLs must be unique")
        return v


class ProfileSearchRequest(BaseModel):
    """Request schema for searching profiles."""

    latitude: float = Field(..., ge=-90, le=90, description="Search center latitude")
    longitude: float = Field(
        ..., ge=-180, le=180, description="Search center longitude"
    )
    radius_km: int = Field(
        50, ge=1, le=200, description="Search radius in kilometers (1-200)"
    )
    age_min: int | None = Field(None, ge=18, le=100, description="Minimum age")
    age_max: int | None = Field(None, ge=18, le=100, description="Maximum age")
    gender: Gender | None = Field(None, description="Preferred gender")


class ProfileSearchResponse(BaseModel):
    """Response schema for profile search results."""

    profiles: list[ProfileResponse] = Field(
        ..., description="List of matching profiles"
    )
    total: int = Field(..., description="Total number of results")
