from enum import Enum


class RoleEnum(str, Enum):
    """User roles with different permission levels"""
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


class RecordTypeEnum(str, Enum):
    """Financial record types"""
    INCOME = "income"
    EXPENSE = "expense"


class CategoryEnum(str, Enum):
    """Financial record categories"""
    SALARY = "salary"
    BONUS = "bonus"
    INVESTMENT = "investment"
    FREELANCE = "freelance"
    FOOD = "food"
    TRANSPORTATION = "transportation"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    SHOPPING = "shopping"
    RENT = "rent"
    OTHER = "other"


class UserStatusEnum(str, Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
