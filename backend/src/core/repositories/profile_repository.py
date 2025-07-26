from abc import ABC, abstractmethod

from src.core.entities.user import UserProfile


class ProfileRepository(ABC):
    """Repository interface for user profile operations."""

    @abstractmethod
    async def create(self, profile: UserProfile) -> UserProfile:
        """Create a new user profile."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> UserProfile | None:
        """Get a user profile by user ID."""
        pass

    @abstractmethod
    async def get_by_id(self, profile_id: int) -> UserProfile | None:
        """Get a user profile by profile ID."""
        pass

    @abstractmethod
    async def update(self, profile: UserProfile) -> UserProfile:
        """Update an existing user profile."""
        pass

    @abstractmethod
    async def delete(self, profile_id: int) -> bool:
        """Delete a user profile."""
        pass

    @abstractmethod
    async def add_picture(self, user_id: int, picture_url: str) -> bool:
        """Add a picture to user's profile."""
        pass

    @abstractmethod
    async def remove_picture(self, user_id: int, picture_url: str) -> bool:
        """Remove a picture from user's profile."""
        pass

    @abstractmethod
    async def get_profiles_by_location_radius(
        self, latitude: float, longitude: float, radius_km: int, exclude_user_id: int
    ) -> list[UserProfile]:
        """Get profiles within a geographic radius."""
        pass
