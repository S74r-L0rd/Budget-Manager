from flask_sqlalchemy import SQLAlchemy
from db import db

# Database model for user profiles
class Profile(db.Model):
    __tablename__ = 'user_profile'

    # id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    dob = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    occupation = db.Column(db.String(50))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()