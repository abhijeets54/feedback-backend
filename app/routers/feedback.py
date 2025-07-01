from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import User, Feedback, FeedbackRequest, UserRole, SentimentType
from app.schemas import (
    Feedback as FeedbackSchema,
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackWithUsers,
    FeedbackRequest as FeedbackRequestSchema,
    FeedbackRequestCreate,
    FeedbackRequestWithUsers,
    DashboardStats,
    FeedbackSummary
)
from app.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=FeedbackSchema)
async def create_feedback(
    feedback_data: FeedbackCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.MANAGER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can create feedback"
        )
    
    # Verify the employee is in the manager's team
    employee = db.query(User).filter(User.id == feedback_data.employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    if employee.manager_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only give feedback to your team members"
        )
    
    db_feedback = Feedback(
        manager_id=current_user.id,
        employee_id=feedback_data.employee_id,
        strengths=feedback_data.strengths,
        areas_to_improve=feedback_data.areas_to_improve,
        overall_sentiment=feedback_data.overall_sentiment
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.get("/", response_model=List[FeedbackWithUsers])
async def get_feedback(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role == UserRole.MANAGER:
        # Managers see feedback they've given
        feedback = db.query(Feedback).filter(Feedback.manager_id == current_user.id).all()
    else:
        # Employees see feedback they've received
        feedback = db.query(Feedback).filter(Feedback.employee_id == current_user.id).all()
    
    return feedback

@router.get("/dashboard", response_model=FeedbackSummary)
async def get_dashboard_data(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role == UserRole.MANAGER:
        # Manager dashboard
        feedback = db.query(Feedback).filter(Feedback.manager_id == current_user.id).all()
        team_members_count = db.query(User).filter(User.manager_id == current_user.id).count()
    else:
        # Employee dashboard
        feedback = db.query(Feedback).filter(Feedback.employee_id == current_user.id).all()
        team_members_count = 0
    
    # Calculate stats
    total_feedback = len(feedback)
    positive_feedback = len([f for f in feedback if f.overall_sentiment == SentimentType.POSITIVE])
    neutral_feedback = len([f for f in feedback if f.overall_sentiment == SentimentType.NEUTRAL])
    negative_feedback = len([f for f in feedback if f.overall_sentiment == SentimentType.NEGATIVE])
    
    stats = DashboardStats(
        total_feedback=total_feedback,
        positive_feedback=positive_feedback,
        neutral_feedback=neutral_feedback,
        negative_feedback=negative_feedback,
        team_members_count=team_members_count
    )
    
    return FeedbackSummary(feedback=feedback, stats=stats)

@router.put("/{feedback_id}", response_model=FeedbackSchema)
async def update_feedback(
    feedback_id: int,
    feedback_update: FeedbackUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    if feedback.manager_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own feedback"
        )
    
    for field, value in feedback_update.dict(exclude_unset=True).items():
        setattr(feedback, field, value)
    
    db.commit()
    db.refresh(feedback)
    return feedback

@router.post("/{feedback_id}/acknowledge")
async def acknowledge_feedback(
    feedback_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    if feedback.employee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only acknowledge feedback given to you"
        )
    
    feedback.acknowledged = True
    feedback.acknowledged_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Feedback acknowledged successfully"}

# Feedback Request endpoints
@router.post("/request", response_model=FeedbackRequestSchema)
async def create_feedback_request(
    request_data: FeedbackRequestCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.EMPLOYEE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can request feedback"
        )

    if not current_user.manager_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have a manager assigned"
        )

    # Check if there's already a pending request
    existing_request = db.query(FeedbackRequest).filter(
        FeedbackRequest.employee_id == current_user.id,
        FeedbackRequest.manager_id == current_user.manager_id,
        FeedbackRequest.status == "pending"
    ).first()

    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a pending feedback request"
        )

    feedback_request = FeedbackRequest(
        employee_id=current_user.id,
        manager_id=current_user.manager_id,
        message=request_data.message,
        status="pending"
    )

    db.add(feedback_request)
    db.commit()
    db.refresh(feedback_request)

    return feedback_request

@router.get("/requests", response_model=List[FeedbackRequestWithUsers])
async def get_feedback_requests(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role == UserRole.MANAGER:
        # Managers see requests from their team members
        requests = db.query(FeedbackRequest).filter(
            FeedbackRequest.manager_id == current_user.id
        ).all()
    else:
        # Employees see their own requests
        requests = db.query(FeedbackRequest).filter(
            FeedbackRequest.employee_id == current_user.id
        ).all()

    return requests

@router.post("/requests/{request_id}/complete")
async def complete_feedback_request(
    request_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    feedback_request = db.query(FeedbackRequest).filter(FeedbackRequest.id == request_id).first()
    if not feedback_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback request not found"
        )

    if feedback_request.manager_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only complete requests assigned to you"
        )

    feedback_request.status = "completed"
    feedback_request.completed_at = datetime.utcnow()
    db.commit()

    return {"message": "Feedback request marked as completed"}

@router.delete("/requests/{request_id}")
async def cancel_feedback_request(
    request_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    feedback_request = db.query(FeedbackRequest).filter(FeedbackRequest.id == request_id).first()
    if not feedback_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback request not found"
        )

    # Both employee and manager can cancel the request
    if feedback_request.employee_id != current_user.id and feedback_request.manager_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only cancel your own requests or requests assigned to you"
        )

    feedback_request.status = "cancelled"
    db.commit()

    return {"message": "Feedback request cancelled"}
