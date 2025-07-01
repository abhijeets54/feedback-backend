from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserRole
from app.schemas import User as UserSchema, UserWithManager, UserUpdate
from app.auth import get_current_active_user

router = APIRouter()

@router.get("/me", response_model=UserWithManager)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/team", response_model=List[UserSchema])
async def get_team_members(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.MANAGER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can view team members"
        )
    
    team_members = db.query(User).filter(User.manager_id == current_user.id).all()
    return team_members

@router.get("/managers", response_model=List[UserSchema])
async def get_managers(db: Session = Depends(get_db)):
    managers = db.query(User).filter(User.role == UserRole.MANAGER).all()
    return managers

@router.put("/me", response_model=UserSchema)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user
