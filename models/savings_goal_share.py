from db import db
from datetime import datetime

class SavingsGoalShare(db.Model):
    __tablename__ = 'savings_goal_shares'
    
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('savings_goals.id'), nullable=False)
    shared_with_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tool_name = db.Column(db.String(100), nullable=False)  # e.g., 'savings_goal', 'future_predictor'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    shared_user = db.relationship(
        "User",
        backref="shared_goals",
        primaryjoin="SavingsGoalShare.shared_with_user_id==User.id"
    )

    goal = db.relationship("SavingsGoal", backref="shared_records")
