from db import db
from datetime import datetime

class BudgetPlan(db.Model):
    __tablename__ = 'budget_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    frequency = db.Column(db.String(20), nullable=False)
    total_limit = db.Column(db.Float, nullable=False)
    category_limits = db.Column(db.JSON, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)