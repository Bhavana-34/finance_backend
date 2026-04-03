from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.models.record import Record
from app.models.user import User
from app.schemas.record import RecordCreate, RecordUpdate, CategoryTotal
from app.enums import RecordTypeEnum, CategoryEnum


def create_record(db: Session, user_id: int, record_data: RecordCreate) -> Record:
    """Create a new financial record"""
    db_record = Record(
        user_id=user_id,
        amount=record_data.amount,
        record_type=record_data.record_type,
        category=record_data.category,
        description=record_data.description,
        transaction_date=record_data.transaction_date
    )
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return db_record


def get_record(db: Session, record_id: int, user_id: int) -> Record:
    """Get a specific record (user can only access their own records)"""
    record = db.query(Record).filter(
        and_(Record.id == record_id, Record.user_id == user_id, Record.is_deleted == False)
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    
    return record


def get_user_records(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    record_type: RecordTypeEnum = None,
    category: CategoryEnum = None,
    start_date: datetime = None,
    end_date: datetime = None
) -> tuple[list[Record], int]:
    """Get all records for a user with filtering and pagination"""
    query = db.query(Record).filter(
        and_(Record.user_id == user_id, Record.is_deleted == False)
    )
    
    # Apply filters
    if record_type:
        query = query.filter(Record.record_type == record_type)
    
    if category:
        query = query.filter(Record.category == category)
    
    if start_date:
        query = query.filter(Record.transaction_date >= start_date)
    
    if end_date:
        query = query.filter(Record.transaction_date <= end_date)
    
    # Get total count before pagination
    total_count = query.count()
    
    # Apply pagination
    records = query.order_by(Record.transaction_date.desc()).offset(skip).limit(limit).all()
    
    return records, total_count


def update_record(db: Session, record_id: int, user_id: int, update_data: RecordUpdate) -> Record:
    """Update a financial record"""
    record = get_record(db, record_id, user_id)
    
    update_dict = update_data.model_dump(exclude_unset=True)
    
    for key, value in update_dict.items():
        setattr(record, key, value)
    
    db.commit()
    db.refresh(record)
    
    return record


def delete_record(db: Session, record_id: int, user_id: int) -> None:
    """Soft delete a financial record"""
    record = get_record(db, record_id, user_id)
    record.is_deleted = True
    db.commit()


def hard_delete_record(db: Session, record_id: int, user_id: int) -> None:
    """Permanently delete a record (admin only)"""
    record = db.query(Record).filter(
        and_(Record.id == record_id, Record.user_id == user_id)
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    
    db.delete(record)
    db.commit()


def calculate_total_income(db: Session, user_id: int) -> float:
    """Calculate total income for a user"""
    result = db.query(func.sum(Record.amount)).filter(
        and_(
            Record.user_id == user_id,
            Record.record_type == RecordTypeEnum.INCOME,
            Record.is_deleted == False
        )
    ).scalar()
    
    return float(result) if result else 0.0


def calculate_total_expenses(db: Session, user_id: int) -> float:
    """Calculate total expenses for a user"""
    result = db.query(func.sum(Record.amount)).filter(
        and_(
            Record.user_id == user_id,
            Record.record_type == RecordTypeEnum.EXPENSE,
            Record.is_deleted == False
        )
    ).scalar()
    
    return float(result) if result else 0.0


def get_category_wise_totals(db: Session, user_id: int) -> dict:
    """Get category-wise totals for a user"""
    results = db.query(
        Record.category,
        func.sum(Record.amount).label("total"),
        func.count(Record.id).label("count")
    ).filter(
        and_(Record.user_id == user_id, Record.is_deleted == False)
    ).group_by(Record.category).all()
    
    category_totals = {}
    for category, total, count in results:
        category_totals[category.value] = {
            "total": float(total),
            "count": count
        }
    
    return category_totals


def get_recent_records(db: Session, user_id: int, limit: int = 5) -> list[Record]:
    """Get recent records for a user"""
    return db.query(Record).filter(
        and_(Record.user_id == user_id, Record.is_deleted == False)
    ).order_by(Record.transaction_date.desc()).limit(limit).all()


def get_monthly_trend(db: Session, user_id: int, months: int = 6) -> dict:
    """Get monthly income/expense trend"""
    from datetime import datetime, timezone
    
    start_date = datetime.now(timezone.utc) - timedelta(days=30 * months)
    
    results = db.query(
        func.strftime('%Y-%m', Record.transaction_date).label("month"),
        Record.record_type,
        func.sum(Record.amount).label("total")
    ).filter(
        and_(
            Record.user_id == user_id,
            Record.transaction_date >= start_date,
            Record.is_deleted == False
        )
    ).group_by(
        func.strftime('%Y-%m', Record.transaction_date),
        Record.record_type
    ).order_by(func.strftime('%Y-%m', Record.transaction_date).desc()).all()
    
    trend = {}
    for month, record_type, total in results:
        if month not in trend:
            trend[month] = {"income": 0.0, "expense": 0.0}
        trend[month][record_type.value] = float(total)
    
    return trend
