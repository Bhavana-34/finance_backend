from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.user import User
from app.schemas.record import RecordCreate, RecordUpdate, RecordResponse
from app.services.record import (
    create_record,
    get_record,
    get_user_records,
    update_record,
    delete_record,
    hard_delete_record
)
from app.core.dependencies import get_current_user, require_role
from app.enums import RoleEnum, RecordTypeEnum, CategoryEnum

router = APIRouter(prefix="/api/records", tags=["records"])


@router.post("", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
def create_financial_record(
    record_data: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.ADMIN, RoleEnum.ANALYST))
):
    """
    Create a new financial record (admin and analyst only)
    
    - **amount**: transaction amount (must be positive)
    - **record_type**: income or expense
    - **category**: transaction category
    - **description**: optional description
    - **transaction_date**: date of transaction
    """
    return create_record(db, current_user.id, record_data)


@router.get("/{record_id}", response_model=RecordResponse)
def get_financial_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific financial record (users can only access their own records)"""
    return get_record(db, record_id, current_user.id)


@router.get("", response_model=dict)
def list_financial_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    record_type: RecordTypeEnum = Query(None),
    category: CategoryEnum = Query(None),
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List financial records with filtering and pagination
    
    - **skip**: number of records to skip
    - **limit**: maximum number of records to return
    - **record_type**: filter by income or expense
    - **category**: filter by category
    - **start_date**: filter records from this date
    - **end_date**: filter records until this date
    """
    records, total_count = get_user_records(
        db,
        current_user.id,
        skip=skip,
        limit=limit,
        record_type=record_type,
        category=category,
        start_date=start_date,
        end_date=end_date
    )
    
    return {
        "records": [RecordResponse.from_orm(r) for r in records],
        "total_count": total_count,
        "skip": skip,
        "limit": limit
    }


@router.put("/{record_id}", response_model=RecordResponse)
def update_financial_record(
    record_id: int,
    update_data: RecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.ADMIN, RoleEnum.ANALYST))
):
    """Update a financial record (admin and analyst only, own records)"""
    return update_record(db, record_id, current_user.id, update_data)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_financial_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.ADMIN, RoleEnum.ANALYST))
):
    """Delete (soft delete) a financial record (admin and analyst only)"""
    delete_record(db, record_id, current_user.id)


@router.delete("/{record_id}/permanent", status_code=status.HTTP_204_NO_CONTENT)
def permanently_delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.ADMIN))
):
    """Permanently delete a record (admin only)"""
    hard_delete_record(db, record_id, current_user.id)
