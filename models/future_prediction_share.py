from db import db
from datetime import datetime

class FuturePredictionShare(db.Model):
    __tablename__ = 'future_prediction_shares'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shared_with_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    prediction_data = db.Column(db.Text, nullable=True)  # JSON string of forecast
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Adding these relationships for easier access
    owner = db.relationship('User', foreign_keys=[owner_id])
    shared_user = db.relationship('User', foreign_keys=[shared_with_user_id])