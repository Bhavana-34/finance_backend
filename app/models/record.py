from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base, get_utc_now
from app.enums import RecordTypeEnum, CategoryEnum


class Record(Base):
    """Financial record model for transactions/entries"""
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    record_type = Column(SQLEnum(RecordTypeEnum), nullable=False, index=True)
    category = Column(SQLEnum(CategoryEnum), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    transaction_date = Column(DateTime, nullable=False, index=True)
    is_deleted = Column(Integer, default=False)  # Soft delete flag
    created_at = Column(DateTime, default=get_utc_now, nullable=False)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now, nullable=False)

    # Relationship to user
    user = relationship("User", back_populates="records")

    def __repr__(self):
        return f"<Record(id={self.id}, user_id={self.user_id}, amount={self.amount}, type={self.record_type})>"
