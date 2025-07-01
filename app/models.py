from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"

class SentimentType(str, enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    manager = relationship("User", remote_side=[id], back_populates="team_members")
    team_members = relationship("User", back_populates="manager")
    given_feedback = relationship("Feedback", foreign_keys="Feedback.manager_id", back_populates="manager")
    received_feedback = relationship("Feedback", foreign_keys="Feedback.employee_id", back_populates="employee")
    sent_feedback_requests = relationship("FeedbackRequest", foreign_keys="FeedbackRequest.employee_id", back_populates="employee")
    received_feedback_requests = relationship("FeedbackRequest", foreign_keys="FeedbackRequest.manager_id", back_populates="manager")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    strengths = Column(Text, nullable=False)
    areas_to_improve = Column(Text, nullable=False)
    overall_sentiment = Column(Enum(SentimentType), nullable=False)
    acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    manager = relationship("User", foreign_keys=[manager_id], back_populates="given_feedback")
    employee = relationship("User", foreign_keys=[employee_id], back_populates="received_feedback")
    comments = relationship("FeedbackComment", back_populates="feedback")

class FeedbackComment(Base):
    __tablename__ = "feedback_comments"

    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(Integer, ForeignKey("feedback.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    feedback = relationship("Feedback", back_populates="comments")
    user = relationship("User")

class FeedbackRequest(Base):
    __tablename__ = "feedback_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=True)  # Optional message from employee
    status = Column(String(20), default="pending")  # pending, completed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    employee = relationship("User", foreign_keys=[employee_id], back_populates="sent_feedback_requests")
    manager = relationship("User", foreign_keys=[manager_id], back_populates="received_feedback_requests")
