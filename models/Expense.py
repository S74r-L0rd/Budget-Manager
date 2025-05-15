from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import db

# Database model for shared expense in expense splitter
class Expense(db.Model):
    __tablename__ = 'expense'
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, nullable=False)
    purpose = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)

    # Properly defining the relationship
    participants = relationship("ExpenseParticipant", back_populates="expense")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()