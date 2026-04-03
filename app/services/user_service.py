from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password
from app.enums import UserStatusEnum
from fastapi import HTTPException, status


def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        or_(User.username == user_data.username, User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Hash password and create user
    hashed_password = hash_password(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role,
        status=UserStatusEnum.ACTIVE
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def get_user_by_id(db: Session, user_id: int) -> User:
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


def get_user_by_username(db: Session, username: str) -> User:
    """Get user by username"""
    user = db.query(User).filter(User.username == username).first()
    return user


def authenticate_user(db: Session, username: str, password: str) -> User:
    """Authenticate user with username and password"""
    user = get_user_by_username(db, username)
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    if user.status.value == "inactive":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


def update_user(db: Session, user_id: int, update_data: UserUpdate) -> User:
    """Update user information"""
    user = get_user_by_id(db, user_id)
    
    update_dict = update_data.model_dump(exclude_unset=True)
    
    if "password" in update_dict and update_dict["password"]:
        update_dict["hashed_password"] = hash_password(update_dict.pop("password"))
    
    for key, value in update_dict.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    
    return user


def list_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    """List all users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()


def delete_user(db: Session, user_id: int) -> None:
    """Delete a user"""
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()


def deactivate_user(db: Session, user_id: int) -> User:
    """Deactivate a user account"""
    user = get_user_by_id(db, user_id)
    user.status = UserStatusEnum.INACTIVE
    db.commit()
    db.refresh(user)
    return user


def activate_user(db: Session, user_id: int) -> User:
    """Activate an inactive user account"""
    user = get_user_by_id(db, user_id)
    user.status = UserStatusEnum.ACTIVE
    db.commit()
    db.refresh(user)
    return user
