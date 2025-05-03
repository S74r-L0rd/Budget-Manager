from flask import request, redirect, url_for, flash, render_template, session
from models.user import User
from db import db

def login_user():
    if request.method == 'POST':
        email = request.form.get('loginEmail')
        password = request.form.get('loginPassword')
        remember_me = True if request.form.get('rememberMe') else False
        
        # find user by email
        user = User.find_by_email(email)
        
        # check if user exists and password is correct
        if user and user.check_password(password):
            # user login successfully, save to session
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_name'] = user.name
            
            # handle "remember me" function
            if remember_me:
                session.permanent = True
            
            return redirect(url_for('dashboard'))
        else:
            flash('login failed, please check your email or password', 'danger')
            
    return render_template('login.html')

def register_user():
    if request.method == 'POST':
        # get form data
        name = request.form.get('signupName')
        email = request.form.get('signupEmail')
        password = request.form.get('signupPassword')
        confirm_password = request.form.get('confirmPassword')
        
        # check if all fields are filled
        if not all([name, email, password, confirm_password]):
            flash('please fill all required fields', 'danger')
            return render_template('login.html')
        
        if password != confirm_password:
            flash('passwords do not match', 'danger')
            return render_template('register.html')
        
        # check if email already exists
        if User.find_by_email(email):
            flash('email already exists', 'warning')
            return render_template('login.html')
        
        # create user and save to db
        new_user = User(name=name, email=email, password=password)
        try:
            new_user.save_to_db()
            flash('registration successful, please login', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'error occurred: {str(e)}', 'danger')
            
    return render_template('login.html')

def forgot_password():
    # TODO: implement forgot password logic
    if request.method == 'POST':
        email = request.form.get('forgotEmail')
        user = User.find_by_email(email)
        
        if user:
            # TODO: send reset password email here
            flash('reset password link has been sent to your email', 'info')
        else:
            flash('email not found', 'warning')
            
    return render_template('login.html')

def logout_user():
    # clear session
    session.clear()
    flash('you have successfully logged out', 'info')
    return redirect(url_for('login'))
