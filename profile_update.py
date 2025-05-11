
from flask import request, redirect, url_for, flash, session
from models.user import User
from models.userProfile import Profile
from db import db

def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash("You must be logged in to update your profile.", "danger")
        return redirect(url_for('login'))

    # Fetch the user and profile from the database
    user = User.query.get(user_id)
    profile = Profile.query.filter_by(user_id=user_id).first()

    # If profile does not exist, create a new one with user data
    if not profile:
        name = user.name if user.name else "Unnamed"
        email = user.email if user.email else "noemail@example.com"
        profile = Profile(user_id=user_id, name=user.name, email=user.email)
        db.session.add(profile)

    # Get data from the form
    name = request.form.get('name', user.name)  # Use existing name if not provided
    email = request.form.get('email', user.email)  # Use existing email if not provided

    # Update both user and profile names and emails
    user.name = name
    profile.name = name
    user.email = email
    profile.email = email

    # Update additional profile fields only if provided
    profile.phone = request.form.get('phone', profile.phone)
    profile.address = request.form.get('address', profile.address)
    profile.dob = request.form.get('dob', profile.dob)
    profile.gender = request.form.get('gender', profile.gender)
    profile.occupation = request.form.get('occupation', profile.occupation)

    # Save changes to both user and profile tables
    db.session.add(user)
    db.session.add(profile)
    db.session.commit()
    flash("Profile updated successfully.", "success")

    return redirect(url_for('profile') + '#profile')