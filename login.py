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



def reset_password():
    if request.method == 'POST':
        # get form data
        email = request.form.get('forgotEmail')
        verification_code = request.form.get('verificationCode')
        new_password = request.form.get('newPassword')
        confirm_new_password = request.form.get('confirmNewPassword')
        
        # check if all fields are filled
        if not all([email, verification_code, new_password, confirm_new_password]):
            flash('please fill all required fields', 'danger')
            # stay at reset password page
            return render_template('login.html', stay_at_reset=True)
        
        # check if passwords match
        if new_password != confirm_new_password:
            flash('passwords do not match', 'danger')
            # clear password fields, keep email and verification code
            flash('clear_password_fields', 'clear_form')
            return render_template('login.html', stay_at_reset=True, email=email, code=verification_code)
        
        # check if verification code is valid
        if 'verification_code' not in session or 'verification_email' not in session:
            flash('verification code has expired, please get a new one', 'warning')
            # clear code field, keep email and password
            flash('clear_code_field', 'clear_form')
            return render_template('login.html', stay_at_reset=True, email=email)
        
        if session['verification_code'] != verification_code or session['verification_email'] != email:
            flash('verification code is not correct, please input again', 'danger')
            # clear code field, keep email and password
            flash('clear_code_field', 'clear_form')
            return render_template('login.html', stay_at_reset=True, email=email)
        
        # find user by email
        user = User.find_by_email(email)
        if not user:
            flash('no account found for this email', 'warning')
            # clear form, but stay at reset password page
            flash('clear_forgot_form', 'clear_form')
            return render_template('login.html', stay_at_reset=True)
        
        # update password
        try:
            user.set_password(new_password)
            db.session.commit()
            # clear verification information in session
            if 'verification_code' in session:
                session.pop('verification_code')
            if 'verification_email' in session:
                session.pop('verification_email')
            
            flash('password reset successfully, please login', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'error occurred: {str(e)}', 'danger')
            return render_template('login.html', stay_at_reset=True, email=email)
    
    return render_template('login.html')

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
