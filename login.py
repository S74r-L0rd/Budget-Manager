from flask import request, redirect, url_for, flash, render_template, session, jsonify
from models.user import User
from db import db
from emailVerification import send_verification_email, generate_verification_code

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
            # use special mark to clear form
            flash('passwords do not match', 'danger')
            flash('clear_signup_form', 'clear_form')
            return render_template('login.html')
        
        # check if email already exists
        if User.find_by_email(email):
            flash('email already exists', 'warning')
            flash('clear_signup_form', 'clear_form')
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
            flash('clear_signup_form', 'clear_form')
            
    return render_template('login.html')

def verify_reset_code():
    """API route, verify reset code"""
    if request.method == 'POST':
        email = request.form.get('email')
        code = request.form.get('code')
        
        if not all([email, code]):
            return jsonify({'status': 'error', 'message': 'please provide email and verification code'}), 400
        
        # check if verification code is valid
        if 'verification_code' not in session or 'verification_email' not in session:
            return jsonify({'status': 'error', 'message': 'verification code has expired, please get a new one'}), 400
        
        if session['verification_code'] != code or session['verification_email'] != email:
            return jsonify({'status': 'error', 'message': 'verification code is not correct'}), 400
        
        # find user by email
        user = User.find_by_email(email)
        if not user:
            return jsonify({'status': 'error', 'message': 'no account found for this email'}), 404
        
        return jsonify({'status': 'success', 'message': 'verification code is correct'}), 200
    
    return jsonify({'status': 'error', 'message': 'unsupported request method'}), 405

def reset_password():
    """API route, reset password"""
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([email, new_password, confirm_password]):
            return jsonify({'status': 'error', 'message': 'please provide all required fields'}), 400
        
        # check if passwords match
        if new_password != confirm_password:
            return jsonify({'status': 'error', 'message': 'passwords do not match'}), 400
        
        # find user by email
        user = User.find_by_email(email)
        if not user:
            return jsonify({'status': 'error', 'message': 'no account found for this email'}), 404
        
        # update password
        try:
            user.set_password(new_password)
            db.session.commit()
            # clear verification information in session
            if 'verification_code' in session:
                session.pop('verification_code')
            if 'verification_email' in session:
                session.pop('verification_email')
            
            return jsonify({'status': 'success', 'message': 'password reset successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': f'error occurred: {str(e)}'}), 500
    
    return jsonify({'status': 'error', 'message': 'unsupported request method'}), 405

def logout_user():
    # clear session
    session.clear()
    flash('you have successfully logged out', 'info')
    return redirect(url_for('login'))

def get_verification_code():
    """API route, return verification code"""
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            return jsonify({'status': 'error', 'message': 'please provide an email address'}), 400
        
        # find user by email
        user = User.find_by_email(email)
        if not user:
            return jsonify({'status': 'error', 'message': 'no account found for this email'}), 404
        
        # generate verification code and send email
        verification_code = generate_verification_code()
        success, msg, _ = send_verification_email(email, 'Reset Password', verification_code)
        
        if success:
            # save verification code to session
            session['verification_code'] = verification_code
            session['verification_email'] = email
            return jsonify({'status': 'success', 'message': 'verification code has been sent to your email'}), 200
        else:
            return jsonify({'status': 'error', 'message': f'failed to send verification code: {msg}'}), 500
    
    return jsonify({'status': 'error', 'message': 'unsupported request method'}), 405
