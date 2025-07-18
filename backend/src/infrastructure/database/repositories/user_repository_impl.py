from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.entities.user import User, UserProfile
from ....core.repositories.user_repository import UserProfileRepository, UserRepository
from ....core.value_objects.age import Age
from ....core.value_objects.email import Email
from ....core.value_objects.fame_rating import FameRating
from ....core.value_objects.location import Location
from ..models.user_model import UserModel, UserProfileModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User) -> User:
        """Create a new user"""
        db_user = UserModel(
            username=user.username,
            email=str(user.email),
            password_hash=user.password_hash,
            first_name=user.first_name,
            last_name=user.last_name,
            status=user.status,
            email_verified=user.email_verified,
            last_seen=user.last_seen,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return self._to_entity(db_user)

    async def get_by_id(self, user_id: int) -> User | None:
        """Get user by ID"""
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email"""
        result = await self.db.execute(
            select(UserModel).where(UserModel.email == email)
        )
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None

    async def get_by_username(self, username: str) -> User | None:
        """Get user by username"""
        result = await self.db.execute(
            select(UserModel).where(UserModel.username == username)
        )
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None

    async def update(self, user: User) -> User:
        """Update user"""
        result = await self.db.execute(select(UserModel).where(UserModel.id == user.id))
        db_user = result.scalar_one_or_none()

        if not db_user:
            raise ValueError(f"User with ID {user.id} not found")

        # Update fields
        db_user.username = user.username
        db_user.email = str(user.email)
        db_user.password_hash = user.password_hash
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db_user.status = user.status
        db_user.email_verified = user.email_verified
        db_user.last_seen = user.last_seen
        db_user.updated_at = user.updated_at

        await self.db.commit()
        await self.db.refresh(db_user)

        return self._to_entity(db_user)

    async def delete(self, user_id: int) -> bool:
        """Delete user"""
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        db_user = result.scalar_one_or_none()

        if not db_user:
            return False

        await self.db.delete(db_user)
        await self.db.commit()
        return True

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[User]:
        """Get all users with pagination"""
        result = await self.db.execute(select(UserModel).offset(offset).limit(limit))
        db_users = result.scalars().all()
        return [self._to_entity(db_user) for db_user in db_users]

    async def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email"""
        result = await self.db.execute(
            select(UserModel.id).where(UserModel.email == email)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_username(self, username: str) -> bool:
        """Check if user exists by username"""
        result = await self.db.execute(
            select(UserModel.id).where(UserModel.username == username)
        )
        return result.scalar_one_or_none() is not None

    def _to_entity(self, db_user: UserModel) -> User:
        """Convert database model to domain entity"""
        return User(
            id=db_user.id,
            username=db_user.username,
            email=Email(db_user.email),
            password_hash=db_user.password_hash,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            status=db_user.status,
            email_verified=db_user.email_verified,
            last_seen=db_user.last_seen,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )


class UserProfileRepositoryImpl(UserProfileRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, profile: UserProfile) -> UserProfile:
        """Create a new user profile"""
        db_profile = UserProfileModel(
            user_id=profile.user_id,
            age=profile.age.value,
            gender=profile.gender.value,
            sexual_preference=profile.sexual_preference.value,
            biography=profile.biography,
            latitude=profile.location.latitude if profile.location else None,
            longitude=profile.location.longitude if profile.location else None,
            city=profile.location.city if profile.location else None,
            country=profile.location.country if profile.location else None,
            fame_rating=profile.fame_rating.value,
            interests=profile.interests,
            pictures=profile.pictures,
            profile_completed=profile.profile_completed,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        )

        self.db.add(db_profile)
        await self.db.commit()
        await self.db.refresh(db_profile)

        return self._to_entity(db_profile)

    async def get_by_id(self, profile_id: int) -> UserProfile | None:
        """Get profile by ID"""
        result = await self.db.execute(
            select(UserProfileModel).where(UserProfileModel.id == profile_id)
        )
        db_profile = result.scalar_one_or_none()
        return self._to_entity(db_profile) if db_profile else None

    async def get_by_user_id(self, user_id: int) -> UserProfile | None:
        """Get profile by user ID"""
        result = await self.db.execute(
            select(UserProfileModel).where(UserProfileModel.user_id == user_id)
        )
        db_profile = result.scalar_one_or_none()
        return self._to_entity(db_profile) if db_profile else None

    async def update(self, profile: UserProfile) -> UserProfile:
        """Update profile"""
        result = await self.db.execute(
            select(UserProfileModel).where(UserProfileModel.id == profile.id)
        )
        db_profile = result.scalar_one_or_none()

        if not db_profile:
            raise ValueError(f"Profile with ID {profile.id} not found")

        # Update fields
        db_profile.age = profile.age.value
        db_profile.gender = profile.gender.value
        db_profile.sexual_preference = profile.sexual_preference.value
        db_profile.biography = profile.biography
        db_profile.latitude = profile.location.latitude if profile.location else None
        db_profile.longitude = profile.location.longitude if profile.location else None
        db_profile.city = profile.location.city if profile.location else None
        db_profile.country = profile.location.country if profile.location else None
        db_profile.fame_rating = profile.fame_rating.value
        db_profile.interests = profile.interests
        db_profile.pictures = profile.pictures
        db_profile.profile_completed = profile.profile_completed
        db_profile.updated_at = profile.updated_at

        await self.db.commit()
        await self.db.refresh(db_profile)

        return self._to_entity(db_profile)

    async def delete(self, profile_id: int) -> bool:
        """Delete profile"""
        result = await self.db.execute(
            select(UserProfileModel).where(UserProfileModel.id == profile_id)
        )
        db_profile = result.scalar_one_or_none()

        if not db_profile:
            return False

        await self.db.delete(db_profile)
        await self.db.commit()
        return True

    async def get_suggestions(self, user_id: int, limit: int = 10) -> list[UserProfile]:
        """Get profile suggestions for user"""
        # For now, return random profiles excluding the user
        result = await self.db.execute(
            select(UserProfileModel)
            .where(UserProfileModel.user_id != user_id)
            .where(UserProfileModel.profile_completed)
            .limit(limit)
        )
        db_profiles = result.scalars().all()
        return [self._to_entity(db_profile) for db_profile in db_profiles]

    async def search_profiles(
        self,
        user_id: int,
        age_min: int = None,
        age_max: int = None,
        max_distance: float = None,
        interests: list[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[UserProfile]:
        """Search profiles with filters"""
        query = select(UserProfileModel).where(UserProfileModel.user_id != user_id)

        if age_min:
            query = query.where(UserProfileModel.age >= age_min)
        if age_max:
            query = query.where(UserProfileModel.age <= age_max)

        # Add more filters as needed

        result = await self.db.execute(query.offset(offset).limit(limit))
        db_profiles = result.scalars().all()
        return [self._to_entity(db_profile) for db_profile in db_profiles]

    async def get_profiles_by_location(
        self, latitude: float, longitude: float, radius_km: float, limit: int = 20
    ) -> list[UserProfile]:
        """Get profiles within a geographic radius"""
        # For now, return all profiles (would need PostGIS for proper geo queries)
        result = await self.db.execute(
            select(UserProfileModel)
            .where(UserProfileModel.latitude.isnot(None))
            .where(UserProfileModel.longitude.isnot(None))
            .limit(limit)
        )
        db_profiles = result.scalars().all()
        return [self._to_entity(db_profile) for db_profile in db_profiles]

    def _to_entity(self, db_profile: UserProfileModel) -> UserProfile:
        """Convert database model to domain entity"""
        location = None
        if db_profile.latitude and db_profile.longitude:
            location = Location(
                latitude=db_profile.latitude,
                longitude=db_profile.longitude,
                city=db_profile.city,
                country=db_profile.country,
            )

        return UserProfile(
            id=db_profile.id,
            user_id=db_profile.user_id,
            age=Age(db_profile.age),
            gender=db_profile.gender,
            sexual_preference=db_profile.sexual_preference,
            biography=db_profile.biography,
            location=location,
            fame_rating=FameRating(db_profile.fame_rating),
            interests=db_profile.interests or [],
            pictures=db_profile.pictures or [],
            profile_completed=db_profile.profile_completed,
            created_at=db_profile.created_at,
            updated_at=db_profile.updated_at,
        )
