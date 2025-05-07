
from flask import request, redirect, url_for, flash, render_template, session
from models.user import User
from models.userProfile import Profile
from db import db

def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = Profile(user_id=user_id)

    # Only update if field is present
    name = request.form.get('name')
    email = request.form.get('email')
    if name: user.name = name
    if email: user.email = email

    # Optional fields that will be updated from Profile
    if 'phone' in request.form:
        profile.phone = request.form.get('phone')
    if 'address' in request.form:
        profile.address = request.form.get('address')
    if 'dob' in request.form:
        profile.dob = request.form.get('dob')
    if 'gender' in request.form:
        profile.gender = request.form.get('gender')
    if 'occupation' in request.form:
        profile.occupation = request.form.get('occupation')

    db.session.add(user)
    db.session.add(profile)
    db.session.commit()

    return redirect(url_for('profile') + '#profile')