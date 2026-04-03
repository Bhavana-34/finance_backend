from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import create_access_token
from app.services.user_service import authenticate_user, create_user, get_user_by_username
from datetime import timedelta


def register_user(db: Session, user_data: UserCreate) -> dict:
    """Register a new user and return token"""
    user = create_user(db, user_data)
    
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=30)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }


def login_user(db: Session, username: str, password: str) -> dict:
    """Login user and return token"""
    user = authenticate_user(db, username, password)
    
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=30)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }
