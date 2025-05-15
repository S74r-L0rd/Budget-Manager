from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import db

# Database model for participants of shared expense
class ExpenseParticipant(db.Model):
    __tablename__ = 'expense_participant'
    id = Column(Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey('expense.id'), nullable=False)
    user_id = Column(Integer, nullable=False)
    amount_paid = Column(Float, default=0.0)
    amount_due = Column(Float, nullable=False)
    status = Column(String, default="Pending")

    # Properly defining the relationship
    expense = relationship("Expense", back_populates="participants")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()