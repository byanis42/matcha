from sqlalchemy import and_, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entities.user import UserProfile
from src.core.repositories.profile_repository import ProfileRepository
from src.core.value_objects.age import Age
from src.core.value_objects.fame_rating import FameRating
from src.core.value_objects.location import Location
from src.infrastructure.database.models.user_model import UserProfileModel


class ProfileRepositoryImpl(ProfileRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _model_to_entity(self, model: UserProfileModel) -> UserProfile:
        """Convert database model to domain entity."""
        location = None
        if model.latitude is not None and model.longitude is not None:
            location = Location(
                latitude=model.latitude,
                longitude=model.longitude,
                city=model.city,
                country=model.country,
            )

        return UserProfile(
            id=model.id,
            user_id=model.user_id,
            age=Age(model.age),
            gender=model.gender,
            sexual_preference=model.sexual_preference,
            biography=model.biography,
            location=location,
            fame_rating=FameRating(model.fame_rating),
            interests=model.interests or [],
            pictures=model.pictures or [],
            profile_completed=model.profile_completed,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _entity_to_model_data(self, profile: UserProfile) -> dict:
        """Convert domain entity to database model data."""
        data = {
            "user_id": profile.user_id,
            "age": profile.age.value,
            "gender": profile.gender.value,
            "sexual_preference": profile.sexual_preference.value,
            "biography": profile.biography,
            "fame_rating": profile.fame_rating.value,
            "interests": profile.interests,
            "pictures": profile.pictures,
            "profile_completed": profile.profile_completed,
        }

        if profile.location:
            data.update(
                {
                    "latitude": profile.location.latitude,
                    "longitude": profile.location.longitude,
                    "city": profile.location.city,
                    "country": profile.location.country,
                }
            )

        return data

    async def create(self, profile: UserProfile) -> UserProfile:
        """Create a new user profile."""
        model_data = self._entity_to_model_data(profile)
        model = UserProfileModel(**model_data)

        self.session.add(model)
        await self.session.flush()

        # Update entity with generated ID
        profile.id = model.id
        return profile

    async def get_by_user_id(self, user_id: int) -> UserProfile | None:
        """Get a user profile by user ID."""
        stmt = select(UserProfileModel).where(UserProfileModel.user_id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._model_to_entity(model)

    async def get_by_id(self, profile_id: int) -> UserProfile | None:
        """Get a user profile by profile ID."""
        stmt = select(UserProfileModel).where(UserProfileModel.id == profile_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._model_to_entity(model)

    async def update(self, profile: UserProfile) -> UserProfile:
        """Update an existing user profile."""
        model_data = self._entity_to_model_data(profile)

        stmt = (
            update(UserProfileModel)
            .where(UserProfileModel.id == profile.id)
            .values(**model_data)
        )
        await self.session.execute(stmt)

        return profile

    async def delete(self, profile_id: int) -> bool:
        """Delete a user profile."""
        stmt = select(UserProfileModel).where(UserProfileModel.id == profile_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return False

        await self.session.delete(model)
        return True

    async def add_picture(self, user_id: int, picture_url: str) -> bool:
        """Add a picture to user's profile."""
        # Get current profile
        profile = await self.get_by_user_id(user_id)
        if profile is None:
            return False

        # Check if picture already exists or limit exceeded
        if picture_url in profile.pictures or len(profile.pictures) >= 5:
            return False

        # Add picture and update
        profile.add_picture(picture_url)
        await self.update(profile)
        return True

    async def remove_picture(self, user_id: int, picture_url: str) -> bool:
        """Remove a picture from user's profile."""
        # Get current profile
        profile = await self.get_by_user_id(user_id)
        if profile is None:
            return False

        # Check if picture exists
        if picture_url not in profile.pictures:
            return False

        # Remove picture and update
        profile.remove_picture(picture_url)
        await self.update(profile)
        return True

    async def get_profiles_by_location_radius(
        self, latitude: float, longitude: float, radius_km: int, exclude_user_id: int
    ) -> list[UserProfile]:
        """Get profiles within a geographic radius using Haversine formula."""
        # Haversine formula to calculate distance
        lat1_rad = func.radians(latitude)
        lng1_rad = func.radians(longitude)
        lat2_rad = func.radians(UserProfileModel.latitude)
        lng2_rad = func.radians(UserProfileModel.longitude)

        dlat = lat2_rad - lat1_rad
        dlng = lng2_rad - lng1_rad

        a = (
            func.sin(dlat / 2) ** 2
            + func.cos(lat1_rad) * func.cos(lat2_rad) * func.sin(dlng / 2) ** 2
        )
        distance = 2 * func.asin(func.sqrt(a)) * 6371  # Earth radius in km

        stmt = select(UserProfileModel).where(
            and_(
                UserProfileModel.user_id != exclude_user_id,
                UserProfileModel.latitude.isnot(None),
                UserProfileModel.longitude.isnot(None),
                distance <= radius_km,
                UserProfileModel.profile_completed == True,  # noqa: E712
            )
        )

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]
