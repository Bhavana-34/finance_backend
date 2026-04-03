from sqlalchemy.orm import Session
from app.services.record import (
    calculate_total_income,
    calculate_total_expenses,
    get_category_wise_totals,
    get_recent_records,
    get_monthly_trend
)
from app.schemas.record import DashboardSummary


def get_dashboard_summary(db: Session, user_id: int) -> DashboardSummary:
    """Get complete dashboard summary for a user"""
    
    total_income = calculate_total_income(db, user_id)
    total_expenses = calculate_total_expenses(db, user_id)
    net_balance = total_income - total_expenses
    category_wise_totals = get_category_wise_totals(db, user_id)
    recent_records = get_recent_records(db, user_id, limit=10)
    monthly_trend = get_monthly_trend(db, user_id, months=6)
    
    # Convert records to response format
    from app.schemas.record import RecordResponse
    recent_records_response = [
        RecordResponse.from_orm(record) for record in recent_records
    ]
    
    return DashboardSummary(
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=net_balance,
        category_wise_totals=category_wise_totals,
        recent_records=recent_records_response,
        monthly_trend=monthly_trend
    )
