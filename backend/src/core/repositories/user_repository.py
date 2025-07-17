from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.user import User, UserProfile


class UserRepository(ABC):
    """Abstract repository for User entity operations"""
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user"""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update user"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """Delete user"""
        pass
    
    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        """Get all users with pagination"""
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email"""
        pass
    
    @abstractmethod
    async def exists_by_username(self, username: str) -> bool:
        """Check if user exists by username"""
        pass


class UserProfileRepository(ABC):
    """Abstract repository for UserProfile entity operations"""
    
    @abstractmethod
    async def create(self, profile: UserProfile) -> UserProfile:
        """Create a new user profile"""
        pass
    
    @abstractmethod
    async def get_by_id(self, profile_id: int) -> Optional[UserProfile]:
        """Get profile by ID"""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[UserProfile]:
        """Get profile by user ID"""
        pass
    
    @abstractmethod
    async def update(self, profile: UserProfile) -> UserProfile:
        """Update profile"""
        pass
    
    @abstractmethod
    async def delete(self, profile_id: int) -> bool:
        """Delete profile"""
        pass
    
    @abstractmethod
    async def get_suggestions(self, user_id: int, limit: int = 10) -> List[UserProfile]:
        """Get profile suggestions for user"""
        pass
    
    @abstractmethod
    async def search_profiles(
        self, 
        user_id: int,
        age_min: int = None,
        age_max: int = None,
        max_distance: float = None,
        interests: List[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[UserProfile]:
        """Search profiles with filters"""
        pass
    
    @abstractmethod
    async def get_profiles_by_location(
        self, 
        latitude: float, 
        longitude: float, 
        radius_km: float,
        limit: int = 20
    ) -> List[UserProfile]:
        """Get profiles within a geographic radius"""
        pass