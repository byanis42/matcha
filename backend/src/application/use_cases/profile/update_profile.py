from src.core.entities.user import Gender, SexualPreference
from src.core.repositories.unit_of_work import AbstractUnitOfWork
from src.core.value_objects.age import Age
from src.core.value_objects.location import Location
from src.shared.exceptions import (
    ForbiddenException,
    NotFoundException,
    ValidationException,
)


class UpdateProfileUseCase:
    """Use case for updating a user profile."""

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        user_id: int,
        profile_id: int | None = None,
        age: int | None = None,
        gender: str | None = None,
        sexual_preference: str | None = None,
        biography: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        city: str | None = None,
        country: str | None = None,
        interests: list[str] | None = None,
    ):
        """Update an existing user profile."""
        async with self.uow:
            # Get profile by user_id or profile_id
            if profile_id is not None:
                profile = await self.uow.profiles.get_by_id(profile_id)
                if profile is None:
                    raise NotFoundException("Profile not found")
                # Check ownership
                if profile.user_id != user_id:
                    raise ForbiddenException("Cannot update another user's profile")
            else:
                profile = await self.uow.profiles.get_by_user_id(user_id)
                if profile is None:
                    raise NotFoundException("Profile not found for user")

            # Update fields if provided
            if age is not None:
                profile.age = Age(age)

            if gender is not None:
                try:
                    profile.gender = Gender(gender)
                except ValueError as e:
                    raise ValidationException(f"Invalid gender: {gender}") from e

            if sexual_preference is not None:
                try:
                    profile.sexual_preference = SexualPreference(sexual_preference)
                except ValueError as e:
                    raise ValidationException(
                        f"Invalid sexual preference: {sexual_preference}"
                    ) from e

            if biography is not None:
                profile.biography = biography

            if interests is not None:
                profile.interests = interests

            # Update location if coordinates provided
            if latitude is not None and longitude is not None:
                profile.location = Location(
                    latitude=latitude,
                    longitude=longitude,
                    city=city,
                    country=country,
                )
            elif latitude is not None or longitude is not None:
                raise ValidationException(
                    "Both latitude and longitude must be provided"
                )

            # Update completion status
            was_previously_complete = profile.profile_completed
            profile.profile_completed = profile.is_complete()

            # Mark user as having completed profile if profile just became complete
            if not was_previously_complete and profile.profile_completed:
                user = await self.uow.users.get_by_id(user_id)
                if user:
                    user.mark_profile_completed()
                    await self.uow.users.update(user)

            # Save changes
            updated_profile = await self.uow.profiles.update(profile)
            await self.uow.commit()

            return updated_profile
