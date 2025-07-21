from abc import ABC, abstractmethod

from src.core.entities.matching import BlockedUser, Like, Match, Report, Visit


class MatchingRepository(ABC):
    """Abstract repository for matching-related operations"""

    @abstractmethod
    async def create_like(self, like: Like) -> Like:
        """Create a new like"""
        pass

    @abstractmethod
    async def get_like(self, user_id: int, target_user_id: int) -> Like | None:
        """Get like between two users"""
        pass

    @abstractmethod
    async def get_likes_by_user(self, user_id: int) -> list[Like]:
        """Get all likes made by a user"""
        pass

    @abstractmethod
    async def get_likes_received(self, user_id: int) -> list[Like]:
        """Get all likes received by a user"""
        pass

    @abstractmethod
    async def update_like(self, like: Like) -> Like:
        """Update a like"""
        pass

    @abstractmethod
    async def delete_like(self, user_id: int, target_user_id: int) -> bool:
        """Delete a like"""
        pass

    @abstractmethod
    async def create_match(self, match: Match) -> Match:
        """Create a new match"""
        pass

    @abstractmethod
    async def get_match(self, user1_id: int, user2_id: int) -> Match | None:
        """Get match between two users"""
        pass

    @abstractmethod
    async def get_matches_by_user(self, user_id: int) -> list[Match]:
        """Get all matches for a user"""
        pass

    @abstractmethod
    async def update_match(self, match: Match) -> Match:
        """Update a match"""
        pass

    @abstractmethod
    async def delete_match(self, match_id: int) -> bool:
        """Delete a match"""
        pass

    @abstractmethod
    async def create_visit(self, visit: Visit) -> Visit:
        """Record a profile visit"""
        pass

    @abstractmethod
    async def get_visits_by_user(self, user_id: int) -> list[Visit]:
        """Get all visits made by a user"""
        pass

    @abstractmethod
    async def get_visits_received(self, user_id: int) -> list[Visit]:
        """Get all visits received by a user"""
        pass

    @abstractmethod
    async def block_user(self, blocked_user: BlockedUser) -> BlockedUser:
        """Block a user"""
        pass

    @abstractmethod
    async def unblock_user(self, user_id: int, blocked_user_id: int) -> bool:
        """Unblock a user"""
        pass

    @abstractmethod
    async def get_blocked_users(self, user_id: int) -> list[BlockedUser]:
        """Get all blocked users for a user"""
        pass

    @abstractmethod
    async def is_user_blocked(self, user_id: int, target_user_id: int) -> bool:
        """Check if user is blocked"""
        pass

    @abstractmethod
    async def create_report(self, report: Report) -> Report:
        """Create a report"""
        pass

    @abstractmethod
    async def get_reports(self, limit: int = 50, offset: int = 0) -> list[Report]:
        """Get all reports with pagination"""
        pass

    @abstractmethod
    async def get_reports_by_user(self, reported_user_id: int) -> list[Report]:
        """Get reports for a specific user"""
        pass

    @abstractmethod
    async def update_report(self, report: Report) -> Report:
        """Update a report"""
        pass
