from sqlalchemy import Column, Integer, String, DateTime, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    merchant = Column(String, nullable=False)
    description = Column(String, nullable=True)
    amount = Column(Numeric(10,2), nullable=False)
    category = Column(String, nullable=False)
    expense_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="expenses")