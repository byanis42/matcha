from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from enum import Enum


class LikeType(str, Enum):
    LIKE = "like"
    SUPER_LIKE = "super_like"
    PASS = "pass"


class Like(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    id: int | None = None
    user_id: int
    target_user_id: int
    like_type: LikeType
    created_at: datetime | None = None
    
    @field_validator('user_id', 'target_user_id')
    @classmethod
    def validate_user_ids(cls, v):
        if v <= 0:
            raise ValueError('User ID must be positive')
        return v
    
    def is_mutual_like(self, other_like: 'Like') -> bool:
        return (
            self.user_id == other_like.target_user_id and
            self.target_user_id == other_like.user_id and
            self.like_type == LikeType.LIKE and
            other_like.like_type == LikeType.LIKE
        )


class MatchStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    REPORTED = "reported"
    DELETED = "deleted"


class Match(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    id: int | None = None
    user1_id: int
    user2_id: int
    status: MatchStatus = MatchStatus.ACTIVE
    matched_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    @field_validator('user1_id', 'user2_id')
    @classmethod
    def validate_user_ids(cls, v):
        if v <= 0:
            raise ValueError('User ID must be positive')
        return v
    
    def involves_user(self, user_id: int) -> bool:
        return user_id in [self.user1_id, self.user2_id]
    
    def get_other_user_id(self, user_id: int) -> int | None:
        if user_id == self.user1_id:
            return self.user2_id
        elif user_id == self.user2_id:
            return self.user1_id
        return None
    
    def is_active(self) -> bool:
        return self.status == MatchStatus.ACTIVE
    
    def block(self) -> None:
        self.status = MatchStatus.BLOCKED
    
    def report(self) -> None:
        self.status = MatchStatus.REPORTED
    
    def delete(self) -> None:
        self.status = MatchStatus.DELETED


class VisitType(str, Enum):
    PROFILE_VIEW = "profile_view"
    PICTURE_VIEW = "picture_view"
    EXTENDED_VIEW = "extended_view"


class Visit(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    id: int | None = None
    visitor_id: int
    visited_user_id: int
    visit_type: VisitType = VisitType.PROFILE_VIEW
    duration_seconds: int | None = None
    created_at: datetime | None = None
    
    @field_validator('visitor_id', 'visited_user_id')
    @classmethod
    def validate_user_ids(cls, v):
        if v <= 0:
            raise ValueError('User ID must be positive')
        return v
    
    @field_validator('duration_seconds')
    @classmethod
    def validate_duration(cls, v):
        if v is not None and v < 0:
            raise ValueError('Duration cannot be negative')
        return v
    
    def is_extended_view(self) -> bool:
        return (
            self.visit_type == VisitType.EXTENDED_VIEW or
            (self.duration_seconds is not None and self.duration_seconds > 30)
        )


class BlockedUser(BaseModel):
    id: int | None = None
    user_id: int
    blocked_user_id: int
    reason: str | None = None
    created_at: datetime | None = None
    
    @field_validator('user_id', 'blocked_user_id')
    @classmethod
    def validate_user_ids(cls, v):
        if v <= 0:
            raise ValueError('User ID must be positive')
        return v
    
    @field_validator('reason')
    @classmethod
    def validate_reason(cls, v):
        if v and len(v) > 500:
            raise ValueError('Reason cannot exceed 500 characters')
        return v


class ReportType(str, Enum):
    INAPPROPRIATE_CONTENT = "inappropriate_content"
    HARASSMENT = "harassment"
    FAKE_PROFILE = "fake_profile"
    SPAM = "spam"
    OTHER = "other"


class Report(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    id: int | None = None
    reporter_id: int
    reported_user_id: int
    report_type: ReportType
    description: str
    resolved: bool = False
    created_at: datetime | None = None
    resolved_at: datetime | None = None
    
    @field_validator('reporter_id', 'reported_user_id')
    @classmethod
    def validate_user_ids(cls, v):
        if v <= 0:
            raise ValueError('User ID must be positive')
        return v
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if not v or len(v) < 10:
            raise ValueError('Description must be at least 10 characters long')
        if len(v) > 1000:
            raise ValueError('Description cannot exceed 1000 characters')
        return v
    
    def resolve(self) -> None:
        self.resolved = True
        self.resolved_at = datetime.utcnow()