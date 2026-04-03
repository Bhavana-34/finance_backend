from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse, UserListResponse
from app.services.user_service import (
    get_user_by_id,
    update_user,
    delete_user,
    list_users,
    deactivate_user,
    activate_user
)
from app.core.dependencies import get_current_user, require_role
from app.enums import RoleEnum

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_current_user(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update current user's information"""
    return update_user(db, current_user.id, update_data)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user by ID (users can only view their own profile, admins can view all)
    """
    # Users can only access their own profile unless they are admin
    if current_user.id != user_id and current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this user"
        )
    
    return get_user_by_id(db, user_id)


@router.get("", response_model=list[UserListResponse])
def list_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.ADMIN))
):
    """
    List all users (admin only)
    
    - **skip**: number of records to skip
    - **limit**: maximum number of records to return
    """
    return list_users(db, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=UserResponse)
def update_user_info(
    user_id: int,
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.ADMIN))
):
    """Update user information (admin only)"""
    return update_user(db, user_id, update_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_account(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.ADMIN))
):
    """Delete a user account (admin only)"""
    delete_user(db, user_id)


@router.post("/{user_id}/deactivate", response_model=UserResponse)
def deactivate_user_account(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.ADMIN))
):
    """Deactivate a user account (admin only)"""
    return deactivate_user(db, user_id)


@router.post("/{user_id}/activate", response_model=UserResponse)
def activate_user_account(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.ADMIN))
):
    """Activate a deactivated user account (admin only)"""
    return activate_user(db, user_id)
