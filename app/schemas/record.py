from pydantic import BaseModel, Field
from app.enums import RecordTypeEnum, CategoryEnum
from datetime import datetime
from typing import Optional


class RecordCreate(BaseModel):
    """Schema for creating a financial record"""
    amount: float = Field(..., gt=0)
    record_type: RecordTypeEnum
    category: CategoryEnum
    description: Optional[str] = Field(None, max_length=500)
    transaction_date: datetime


class RecordUpdate(BaseModel):
    """Schema for updating a financial record"""
    amount: Optional[float] = Field(None, gt=0)
    record_type: Optional[RecordTypeEnum] = None
    category: Optional[CategoryEnum] = None
    description: Optional[str] = Field(None, max_length=500)
    transaction_date: Optional[datetime] = None


class RecordResponse(BaseModel):
    """Schema for record response"""
    id: int
    user_id: int
    amount: float
    record_type: RecordTypeEnum
    category: CategoryEnum
    description: Optional[str]
    transaction_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DashboardSummary(BaseModel):
    """Schema for dashboard summary analytics"""
    total_income: float
    total_expenses: float
    net_balance: float
    category_wise_totals: dict
    recent_records: list[RecordResponse]
    monthly_trend: dict


class CategoryTotal(BaseModel):
    """Schema for category-wise totals"""
    category: CategoryEnum
    total: float
    count: int
