from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from datetime import timedelta
from db import init_db, db
import pandas as pd
import plotly.express as px
from login import login_user, register_user, logout_user, reset_password, get_verification_code
from profile_update import update_profile
from models.user import User
from models.userProfile import Profile
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-very-secret-key'  # Replace with a strong secret in production
# set session lifetime to 7 days
app.permanent_session_lifetime = timedelta(days=7)

CATEGORIES = ["Rent", "Travel", "Entertainment", "Utilities", "Groceries",
              "Insurance", "Debt Repayments", "Loan", "Medical"]

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
    tools = [
        {
            'name': 'Expense Tracker',
            'description': 'Track your daily expenses and budgets.',
            'icon': 'expense.png',
            'route': 'expense_tracker'  
        },
        {
            'name': 'Budget Planner',
            'description': 'Plan your timely budgets easily.',
            'icon': 'budget.png',
            'route': 'budget_planner'
        },
        {
            'name': 'Savings Goal Tracker',
            'description': 'Set and track custom savings goals.',
            'icon': 'saving.png',
            'route': 'savings_goal_tracker'
        },
        {
            'name': 'Future Expense Predictor',
            'description': 'Get AI-powered predictions based on expense history.',
            'icon': 'expense-prediction.png',
            'route': 'future_expense_predictor'
        },
        {
            'name': 'Spending Personality Analyzer',
            'description': 'Discover your spending habits.',
            'icon': 'spending-personality.png',
            'route': 'spending_personality_analyzer'
        },
        {
            'name': 'Expense Splitter',
            'description': 'Split bills with roommates or friends.',
            'icon': 'expense-split.png',
            'route': 'expense_splitter'
        }
    ]
    return render_template('analysis.html', tools=tools)

@app.route('/expense-tracker')
@login_required_custom
def expense_tracker():
    return render_template('expense_tracker.html')

@app.route('/download-template')
def download_template():
    return send_file('templates/expense_template.xlsx', as_attachment=True)

@app.route('/upload-expenses', methods=['POST'])
def upload_expenses():
    file = request.files['file']
    if file and file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
        # basic validation
        if not {'Date', 'Category', 'Description', 'Amount', 'Payment Method'}.issubset(df.columns):
            return render_template('invalid_template.html')

        # Generate charts
        pie = px.pie(df, values='Amount', names='Category', title='Spending by Category')
        bar = px.bar(df.groupby('Category')['Amount'].sum().nlargest(5).reset_index(), x='Category', y='Amount', title='Top 5 Categories')
        line = px.line(df.groupby('Date')['Amount'].sum().reset_index(), x='Date', y='Amount', title='Spending Over Time')

        charts = {
            "pie_chart": pie.to_html(full_html=False),
            "bar_chart": bar.to_html(full_html=False),
            "line_chart": line.to_html(full_html=False),
        }

        return render_template('expense_tracker.html', charts=charts, scroll_to_results=True)

    return redirect(url_for('expense_tracker'))

@app.route('/budget-planner', methods=['GET'])
@login_required_custom
def budget_planner():
    user_id = session.get('user_id')

    # Simulate a saved budget
    mock_budget = {
        'period': 'monthly',
        'total_limit': 3000,
        'category_limits': {
            "Rent": 1000,
            "Travel": 300,
            "Entertainment": 200,
            "Utilities": 250,
            "Groceries": 400,
            "Insurance": 200,
            "Debt Repayments": 300,
            "Loan": 250,
            "Medical": 100
        }
    }
    return render_template('budget_planner.html', categories=CATEGORIES, has_budget=True, budget=mock_budget)

@app.route('/upload-budget-expenses', methods=['POST'])
@login_required_custom
def upload_budget_expenses():
    # This is where you'll compare uploaded expenses with stored budget
    pass  # placeholder

@app.route('/savings-goal-tracker')
@login_required_custom
def savings_goal_tracker():
    return render_template('savings_goal_tracker.html')

@app.route('/future-expense-predictor')
@login_required_custom
def future_expense_predictor():
    return render_template('future_expense_predictor.html')

@app.route('/spending-personality-analyzer')
@login_required_custom
def spending_personality_analyzer():
    return render_template('spending_personality_analyzer.html')

@app.route('/expense-splitter')
@login_required_custom
def expense_splitter():
    return render_template('expense_splitter.html')

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

if __name__ == '__main__':
    app.run(debug=True)
