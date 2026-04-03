from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.record import DashboardSummary
from app.services.analytics_service import get_dashboard_summary
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get complete dashboard summary for the current user
    
    Returns:
    - **total_income**: total income amount
    - **total_expenses**: total expenses amount
    - **net_balance**: net balance (income - expenses)
    - **category_wise_totals**: breakdown by category
    - **recent_records**: last 10 transactions
    - **monthly_trend**: 6-month income/expense trend
    """
    return get_dashboard_summary(db, current_user.id)
