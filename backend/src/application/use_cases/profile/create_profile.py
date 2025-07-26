from src.core.entities.user import Gender, SexualPreference, UserProfile
from src.core.repositories.unit_of_work import AbstractUnitOfWork
from src.core.value_objects.age import Age
from src.core.value_objects.location import Location
from src.shared.exceptions import (
    NotFoundException,
    ValidationException,
)


class CreateProfileUseCase:
    """Use case for creating a user profile."""

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        user_id: int,
        age: int,
        gender: str,
        sexual_preference: str,
        biography: str,
        latitude: float | None = None,
        longitude: float | None = None,
        city: str | None = None,
        country: str | None = None,
        interests: list[str] | None = None,
    ) -> UserProfile:
        """Create a new user profile."""
        async with self.uow:
            # Verify user exists
            user = await self.uow.users.get_by_id(user_id)
            if user is None:
                raise NotFoundException("User not found")

            # Check if profile already exists
            existing_profile = await self.uow.profiles.get_by_user_id(user_id)
            if existing_profile is not None:
                raise ValidationException("User already has a profile")

            # Validate enums
            try:
                gender_enum = Gender(gender)
                preference_enum = SexualPreference(sexual_preference)
            except ValueError as e:
                raise ValidationException(f"Invalid enum value: {e}") from e

            # Create location if coordinates provided
            location = None
            if latitude is not None and longitude is not None:
                location = Location(
                    latitude=latitude,
                    longitude=longitude,
                    city=city,
                    country=country,
                )

            # Create profile entity
            profile = UserProfile(
                user_id=user_id,
                age=Age(age),
                gender=gender_enum,
                sexual_preference=preference_enum,
                biography=biography,
                location=location,
                interests=interests or [],
            )

            # Check if profile is complete
            profile.profile_completed = profile.is_complete()

            # Save profile
            created_profile = await self.uow.profiles.create(profile)

            # Mark user as having completed profile if profile is complete
            if profile.profile_completed:
                user.mark_profile_completed()
                await self.uow.users.update(user)

            await self.uow.commit()

            return created_profile
