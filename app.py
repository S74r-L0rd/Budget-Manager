from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import timedelta
from db import init_db, db
from login import login_user, register_user, logout_user, reset_password, get_verification_code
from profile_update import update_profile
from models.user import User
from models.userProfile import Profile
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-very-secret-key'  # Replace with a strong secret in production
# set session lifetime to 7 days
app.permanent_session_lifetime = timedelta(days=7)

# init db
init_db(app)

# custom login required decorator
# this decorator is used to check if the user is logged in
def login_required_custom(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('please login first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return login_user()
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    return register_user()

@app.route('/get_verification_code', methods=['POST'])
def get_code():
    return get_verification_code()

@app.route('/verify-reset-code', methods=['POST'])
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

@app.route('/reset-password', methods=['POST'])
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

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.clear()  # Clear user session
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required_custom
def dashboard():
    return render_template('dashboard.html')

@app.route('/analysis')
@login_required_custom
def analysis():
    return render_template('analysis.html')

@app.route('/share')
@login_required_custom
def share():
    return render_template('share.html')

# Profile route
@app.route('/profile')
@login_required_custom
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    user = User.query.get(user_id)
    profile = Profile.query.filter_by(user_id=user_id).first()
    return render_template('profile.html', user=user, profile=profile)

# Update Profile route
@app.route('/update-prof', methods=['POST'])
def update_prof():
    return update_profile()


# Change password from profile page
@app.route('/change_password', methods=['POST'])
def change_password():
    user_id = session.get('user_id')
    if not user_id:
        flash("You need to log in to update your password.", "danger")
        return redirect(url_for('login'))

    # Get current password, new password, and confirm password
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # New password and Confirm password should match
    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for('profile'))

    user = User.query.get(user_id)

    # Check if the current password is valid
    if not check_password_hash(user.password_hash, current_password):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for('profile'))

    # Update the password and save to the database
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    #Logout after changing password
    session.pop('user_id', None) #Log out the user without clearing other session data
    flash("Password successfully updated. Please log in again.", "success")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
