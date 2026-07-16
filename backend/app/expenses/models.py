from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    name = Column(String)
    amount = Column(Float)
    category = Column(String)
    date = Column(Date)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="expenses")