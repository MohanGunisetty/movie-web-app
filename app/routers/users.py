from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import database, models, schemas
from ..dependencies import get_current_user, require_admin

router = APIRouter(
    prefix="/api",
    tags=["Users"]
)

# User Routes
@router.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# Admin Routes
@router.get("/admin/users", response_model=List[schemas.UserResponse])
def read_all_users(
    skip: int = 0, 
    limit: int = 100, 
    current_user: models.User = Depends(require_admin), 
    db: Session = Depends(database.get_db)
):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.put("/admin/users/{user_id}/block", response_model=schemas.UserResponse)
def block_user(
    user_id: int, 
    is_active: bool,
    current_user: models.User = Depends(require_admin), 
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prvent admin from blocking themselves
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot block yourself")
        
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user
