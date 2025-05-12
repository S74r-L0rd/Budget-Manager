from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from datetime import timedelta
from db import init_db, db
import pandas as pd
import plotly.express as px
from login import login_user, register_user, logout_user, reset_password, get_verification_code
from profile_update import update_profile
from spending_personality_analyzer import spending_personality
from models.user import User
from models.userProfile import Profile
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from models.budgetPlan import BudgetPlan
import json


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
            return render_template('invalid_template.html', back_url=url_for('expense_tracker'))

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

@app.route('/budget-planner', methods=['GET', 'POST'])
@login_required_custom
def budget_planner():
    user_id = session.get('user_id')

    if request.method == 'POST':
        frequency = request.form.get('frequency')
        total_limit = float(request.form.get('total_limit'))

        category_limits = {cat: float(request.form.get(cat, 0)) for cat in CATEGORIES}

        # Either create or update
        budget = BudgetPlan.query.filter_by(user_id=user_id).first()
        if not budget:
            budget = BudgetPlan(
                user_id=user_id,
                frequency=frequency,
                total_limit=total_limit,
                category_limits=category_limits
            )
            db.session.add(budget)
        else:
            budget.frequency = frequency
            budget.total_limit = total_limit
            budget.category_limits = category_limits

        db.session.commit()
        return redirect(url_for('budget_saved_success'))
    
    # GET logic
    budget = BudgetPlan.query.filter_by(user_id=user_id).first()
    has_budget = bool(budget)
    return render_template('budget_planner.html', categories=CATEGORIES, has_budget=has_budget, budget=budget)

@app.route('/budget-planner/edit', methods=['GET'])
@login_required_custom
def edit_budget_plan():
    user_id = session.get('user_id')
    from models.budgetPlan import BudgetPlan

    budget = BudgetPlan.query.filter_by(user_id=user_id).first()

    if not budget:
        flash("No existing budget found to edit.", "warning")
        return redirect(url_for('budget_planner'))

    return render_template('edit_budget.html', budget=budget, categories=CATEGORIES)

@app.route('/update-budget', methods=['POST'])
@login_required_custom
def update_budget():
    user_id = session.get('user_id')
    frequency = request.form.get('frequency')
    total_limit = float(request.form.get('total_limit'))

    category_limits = {cat: float(request.form.get(cat, 0)) for cat in CATEGORIES}

    budget = BudgetPlan.query.filter_by(user_id=user_id).first()

    if not budget:
        return redirect(url_for('budget_planner'))

    budget.frequency = frequency
    budget.total_limit = total_limit
    budget.category_limits = category_limits

    db.session.commit()
    return redirect(url_for('budget_saved_success'))

@app.route('/budget-planner/success')
@login_required_custom
def budget_saved_success():
    return render_template('budget_saved_success.html')

@app.route('/upload-budget-expenses', methods=['POST'])
@login_required_custom
def upload_budget_expenses():
    user_id = session.get('user_id')
    file = request.files.get('file')

    if not file or not file.filename.endswith('.xlsx'):
        flash("❌ Please upload a valid Excel (.xlsx) file.", "danger")
        return render_template('invalid_template.html', back_url=url_for('budget_planner'))

    try:
        df = pd.read_excel(file)

        # Validate structure
        required_columns = {'Date', 'Category', 'Amount'}
        if not required_columns.issubset(df.columns):
            flash("❌ Invalid Excel format. Required columns: Date, Category, Amount.", "danger")
            return render_template('invalid_template.html', back_url=url_for('budget_planner'))

        # Load saved budget
        budget = BudgetPlan.query.filter_by(user_id=user_id).first()
        if not budget:
            flash("❌ No budget plan found. Please set your budget first.", "warning")
            return redirect(url_for('budget_planner'))

        # Clean and process DataFrame
        df = df[df['Category'].isin(CATEGORIES)]
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df.dropna(subset=['Amount'], inplace=True)

        # Save processed data in session for frequency toggle support
        session['uploaded_expense_df'] = df.to_json(orient='records')
        session['selected_frequency'] = budget.frequency  # You can default to 'monthly' if preferred

        # Redirect to the frequency-based analysis view using user's selected frequency
        return redirect(url_for('budget_frequency_view', frequency=budget.frequency))

    except Exception as e:
        flash(f"❌ Error processing file: {str(e)}", "danger")
        return redirect(url_for('budget_planner'))
    
@app.route('/budget-planner/view/<frequency>')
@login_required_custom
def budget_frequency_view(frequency):
    import json
    from flask import request

    user_id = session.get('user_id')
    budget = BudgetPlan.query.filter_by(user_id=user_id).first()

    if not budget or 'uploaded_expense_df' not in session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Missing budget or uploaded data'}), 400
        flash("Missing budget or uploaded data", "warning")
        return redirect(url_for('budget_planner'))

    df = pd.DataFrame(json.loads(session['uploaded_expense_df']))

    # Normalize based on frequency
    freq_divider = {'daily': 365, 'weekly': 52, 'monthly': 12, 'yearly': 1}
    factor = freq_divider.get(frequency, 12)

    summary = []
    for cat in CATEGORIES:
        spent = df[df['Category'] == cat]['Amount'].sum() * factor
        limit = budget.category_limits.get(cat, 0)
        remaining = limit - spent
        summary.append({
            'category': cat,
            'limit': limit,
            'spent': round(spent, 2),
            'remaining': round(remaining, 2),
            'status': 'Over' if remaining < 0 else 'Under'
        })

    # Generate chart
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Spent', x=[s['category'] for s in summary], y=[s['spent'] for s in summary]))
    fig.add_trace(go.Bar(name='Limit', x=[s['category'] for s in summary], y=[s['limit'] for s in summary]))
    fig.update_layout(barmode='group', title=f'Budget vs Actual ({frequency.title()})')

    # AJAX (fetch) request: return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'summary': summary,
            'plot_data': fig.to_plotly_json()['data'],
            'plot_layout': fig.to_plotly_json()['layout'],
            'frequency': frequency
        })

    # Normal full-page render
    return render_template('budget_planner.html',
                           categories=CATEGORIES,
                           has_budget=True,
                           budget=budget,
                           summary=summary,
                           chart=fig.to_html(full_html=False),
                           active_frequency=frequency,
                           step='result',
                           scroll_target_id='budget-planner-results')

@app.route('/savings-goal-tracker')
@login_required_custom
def savings_goal_tracker():
    return render_template('savings_goal_tracker.html')

@app.route('/future-expense-predictor')
@login_required_custom
def future_expense_predictor():
    return render_template('future_expense_predictor.html')

@app.route('/spending-personality-analyzer', methods=['GET', 'POST'])
@login_required_custom
def spending_personality_analyzer():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename.endswith('.xlsx'):
            flash("❌ Please upload a valid Excel (.xlsx) file.", "danger")
            return render_template('invalid_template.html', back_url=url_for('spending_personality_analyzer'))

        try:
            # Load user's uploaded data
            user_df = pd.read_excel(file)

            # Check for required columns
            required_cols = {'Date', 'Category', 'Amount'}
            if not required_cols.issubset(user_df.columns):
                flash("❌ Invalid Excel format. Required columns: Date, Category, Amount.", "danger")
                return render_template('invalid_template.html', back_url=url_for('spending_personality_analyzer'))
            
            # Load demographic spending data
            demographic_df = pd.read_csv('base_demographic_spending.csv')

            # Run clustering
            cluster_label, insights, bar_chart = spending_personality(user_df, demographic_df)

            return render_template(
                    'spending_personality_analyzer.html',
                    cluster_name=cluster_label,
                    insights=insights,
                    bar_chart=json.dumps(bar_chart),
                    is_loaded=True,
                    scroll_to_results=True
                )

        except Exception as e:
            flash(f"❌ Error processing file: {str(e)}", "danger")
            return redirect(url_for('spending_personality_analyzer'))

    return render_template(
        'spending_personality_analyzer.html',
        insights=[],
        cluster_name="No data",
        bar_chart={},
        is_loaded=False
    )


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
