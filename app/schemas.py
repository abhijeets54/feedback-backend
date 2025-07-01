from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models import UserRole, SentimentType

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    manager_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    manager_id: Optional[int] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserWithManager(User):
    manager: Optional[User] = None

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Feedback schemas
class FeedbackBase(BaseModel):
    employee_id: int
    strengths: str
    areas_to_improve: str
    overall_sentiment: SentimentType

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(BaseModel):
    strengths: Optional[str] = None
    areas_to_improve: Optional[str] = None
    overall_sentiment: Optional[SentimentType] = None

class Feedback(FeedbackBase):
    id: int
    manager_id: int
    acknowledged: bool
    acknowledged_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FeedbackWithUsers(Feedback):
    manager: User
    employee: User

# Feedback comment schemas
class FeedbackCommentBase(BaseModel):
    comment: str

class FeedbackCommentCreate(FeedbackCommentBase):
    feedback_id: int

class FeedbackComment(FeedbackCommentBase):
    id: int
    feedback_id: int
    user_id: int
    created_at: datetime
    user: User

    class Config:
        from_attributes = True

# Dashboard schemas
class DashboardStats(BaseModel):
    total_feedback: int
    positive_feedback: int
    neutral_feedback: int
    negative_feedback: int
    team_members_count: int

class FeedbackSummary(BaseModel):
    feedback: List[FeedbackWithUsers]
    stats: DashboardStats

# Feedback request schemas
class FeedbackRequestBase(BaseModel):
    message: Optional[str] = None

class FeedbackRequestCreate(FeedbackRequestBase):
    pass

class FeedbackRequest(FeedbackRequestBase):
    id: int
    employee_id: int
    manager_id: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FeedbackRequestWithUsers(FeedbackRequest):
    employee: User
    manager: User
