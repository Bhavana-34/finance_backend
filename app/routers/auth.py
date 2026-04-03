from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import register_user, login_user
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/api/auth", tags=["authentication"])


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str


class AuthResponse(BaseModel):
    """Authentication response with token"""
    access_token: str
    token_type: str
    user_id: int
    username: str


@router.post("/register", response_model=AuthResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - **username**: unique username (min 3 characters)
    - **email**: valid email address
    - **password**: password (min 6 characters)
    - **role**: user role (viewer, analyst, admin) - defaults to viewer
    """
    return register_user(db, user_data)


@router.post("/login", response_model=AuthResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with username and password
    
    Returns JWT token for authenticated requests
    """
    return login_user(db, credentials.username, credentials.password)
