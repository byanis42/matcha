from src.core.entities.user import UserProfile
from src.core.repositories.unit_of_work import AbstractUnitOfWork
from src.shared.exceptions import NotFoundException


class GetProfileUseCase:
    """Use case for retrieving a user profile."""

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(self, user_id: int) -> UserProfile:
        """Get a user profile by user ID."""
        async with self.uow:
            profile = await self.uow.profiles.get_by_user_id(user_id)
            if profile is None:
                raise NotFoundException("Profile not found")

            return profile


class GetUserProfileUseCase:
    """Use case for viewing another user's profile."""

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def execute(self, viewer_user_id: int, target_user_id: int) -> UserProfile:
        """Get another user's profile (for viewing/matching purposes)."""
        async with self.uow:
            # Verify viewer exists and has a complete profile
            viewer_profile = await self.uow.profiles.get_by_user_id(viewer_user_id)
            if viewer_profile is None or not viewer_profile.profile_completed:
                raise NotFoundException("Viewer must have a complete profile")

            # Get target profile
            target_profile = await self.uow.profiles.get_by_user_id(target_user_id)
            if target_profile is None:
                raise NotFoundException("User profile not found")

            # Only show completed profiles
            if not target_profile.profile_completed:
                raise NotFoundException("User profile not available")

            return target_profile
