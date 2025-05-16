from db import db
from datetime import datetime

class SpendingPersonalityShare(db.Model):
    __tablename__ = 'spending_personality_shares'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shared_with_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cluster_name = db.Column(db.String(100))
    top_insights = db.Column(db.Text)  # JSON string of top 3 insights
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner = db.relationship('User', foreign_keys=[owner_id], backref='spending_shares_owned')
    shared_user = db.relationship('User', foreign_keys=[shared_with_user_id], backref='spending_shares_received')
