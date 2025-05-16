from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from datetime import timedelta, datetime
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
from werkzeug.utils import secure_filename
from models.budgetPlan import BudgetPlan
from models.savings_goal import SavingsGoal
from models.savings_goal_share import SavingsGoalShare
from models.Expense import Expense
from models.ExpenseParticipant import ExpenseParticipant
from models.future_prediction_share import FuturePredictionShare
import json
import os
from os import getenv
from dotenv import load_dotenv

# load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-very-secret-key'  # Replace with a strong secret in production
# set session lifetime to 7 days
app.permanent_session_lifetime = timedelta(days=7)

CATEGORIES = ["Rent", "Travel", "Entertainment", "Utilities", "Groceries",
              "Insurance", "Debt Repayments", "Loan", "Medical"]

# Config for uploading photo
UPLOAD_FOLDER = 'static/media/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

def generate_summary(forecast_series):
    recent = forecast_series.iloc[-3:]
    direction = recent.diff().mean()

    if direction > 0:
        return "⚠️ Your future expenses are trending upward. Consider revisiting your budget!"
    elif direction < 0:
        return "✅ Great! Your future expenses show a decreasing trend. Keep up the good work!"
    else:
        return "ℹ️ Your expenses seem stable. Monitor regularly to stay on track."

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/contact')
def contact():
    if 'user_id' in session:
        return render_template('contact.html', layout='layout_user.html')
    return render_template('contact.html', layout='layout.html')

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
    user_id = session.get('user_id')
    username = session.get('user_name', 'User')
    
    # get budget plan
    budget = BudgetPlan.query.filter_by(user_id=user_id).first()
    
    return render_template('dashboard.html', budget=budget, username=username)

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

@app.route('/savings-goal-tracker', methods=['GET', 'POST'])
@login_required_custom
def savings_goal_tracker():
    user_id = session.get('user_id')
    
    if request.method == 'POST':

        deadline_str = request.form['deadline']
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        saved_amount = float(request.form['saved_amount'])

        goal = SavingsGoal(
            user_id=user_id,
            goal_name=request.form['goal_name'],
            target_amount=float(request.form['target_amount']),
            saved_amount=saved_amount,
            deadline=deadline
        )
        db.session.add(goal)
        db.session.commit()

        # Handle sharing
        share_with_ids = request.form.getlist('share_with')
        for shared_id in share_with_ids:
            share = SavingsGoalShare(
                goal_id=goal.id,
                shared_with_user_id=int(shared_id),
                tool_name='savings_goal'  # <---- Add this line
            )
            db.session.add(share)
        db.session.commit()
        flash("Goal added and shared!", "success")
        return redirect(url_for('savings_goal_tracker'))

    # Your own goals + goals shared with you
    own_goals = SavingsGoal.query.filter_by(user_id=user_id).all()
    shared_goal_ids = [s.goal_id for s in SavingsGoalShare.query.filter_by(shared_with_user_id=user_id).all()]
    shared_goals = SavingsGoal.query.filter(SavingsGoal.id.in_(shared_goal_ids)).all()
    
    all_users = User.query.filter(User.id != user_id).all()
    return render_template('savings_goal_tracker.html', own_goals=own_goals, shared_goals=shared_goals, users=all_users)

@app.route('/savings-goal/success')
@login_required_custom
def savings_goal_success():
    goal_id = request.args.get('goal_id', type=int)
    return render_template('savings_goal_success.html', goal_id=goal_id)

@app.route("/edit-goal/<int:goal_id>", methods=["GET", "POST"])
@login_required_custom
def edit_savings_goal(goal_id):
    user_id = session.get('user_id')
    goal = SavingsGoal.query.filter_by(id=goal_id, user_id=user_id).first_or_404()

    if request.method == "POST":
        goal.goal_name = request.form["goal_name"]
        goal.target_amount = float(request.form["target_amount"])
        goal.saved_amount = float(request.form["saved_amount"])
        goal.deadline = datetime.strptime(request.form["deadline"], "%Y-%m-%d").date()

        # Update shared users
        db.session.query(SavingsGoalShare).filter_by(goal_id=goal.id).delete()
        share_with_ids = request.form.getlist("share_with")
        for shared_id in share_with_ids:
            share = SavingsGoalShare(
                goal_id=goal.id,
                shared_with_user_id=int(shared_id),
                tool_name='savings_goal'
            )
            db.session.add(share)

        db.session.commit()
        flash("✅ Goal updated successfully!", "success")
        return redirect(url_for("savings_goal_success", goal_id=goal.id))

    users = User.query.filter(User.id != user_id).all()
    shared_user_ids = [share.shared_user.id for share in goal.shares]
    return render_template("edit_goal.html", goal=goal, users=users, shared_user_ids=shared_user_ids)

@app.route('/future-expense-predictor', methods=['GET', 'POST'])
@login_required_custom
def future_expense_predictor():
    from models.future_prediction_share import FuturePredictionShare  # ensure this model is defined

    user_id = session.get('user_id')

    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            df = pd.read_excel(file)

            if not {'Date', 'Category', 'Amount'}.issubset(df.columns):
                flash("Invalid file format", "danger")
                return redirect(url_for('future_expense_predictor'))

            # Preprocess
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.groupby('Date').sum().resample('M').sum().reset_index()

            # Simple prediction (e.g. Linear Regression)
            from sklearn.linear_model import LinearRegression
            import numpy as np
            df['Timestamp'] = df['Date'].map(datetime.toordinal)
            X = df[['Timestamp']]
            y = df['Amount']

            model = LinearRegression()
            model.fit(X, y)

            # Predict for next 6 months
            future_dates = pd.date_range(df['Date'].max(), periods=7, freq='M')[1:]
            future_df = pd.DataFrame({'Date': future_dates})
            future_df['Timestamp'] = future_df['Date'].map(datetime.toordinal)
            future_df['Amount'] = model.predict(future_df[['Timestamp']])
            forecast_series = future_df['Amount']
            summary = generate_summary(forecast_series)

            # Plot
            import plotly.graph_objs as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Amount'], name='Historical'))
            fig.add_trace(go.Scatter(x=future_df['Date'], y=future_df['Amount'], name='Predicted', line=dict(dash='dash')))
            fig.update_layout(title='Future Expense Prediction', xaxis_title='Date', yaxis_title='Amount')
            chart = fig.to_html(full_html=False)

            # Fetch future prediction shares using new model
            shared_by_me = FuturePredictionShare.query.filter_by(owner_id=user_id).all()
            shared_with_me = FuturePredictionShare.query.filter_by(shared_with_user_id=user_id).all()
            users = User.query.filter(User.id != user_id).all()

            return render_template('future_expense_predictor.html',
                                   chart=chart,
                                   show_results=True,
                                   summary=summary,
                                   shared_by_me=shared_by_me,
                                   shared_with_me=shared_with_me,
                                   users=users)

    # On GET: retrieve share info using new model
    shared_by_me = FuturePredictionShare.query.filter_by(owner_id=user_id).all()
    shared_with_me = FuturePredictionShare.query.filter_by(shared_with_user_id=user_id).all()
    users = User.query.filter(User.id != user_id).all()

    return render_template('future_expense_predictor.html',
                           show_results=False,
                           shared_by_me=shared_by_me,
                           shared_with_me=shared_with_me,
                           users=users)

@app.route('/share-future-prediction', methods=['POST'])
@login_required_custom
def share_future_prediction():
    user_id = session.get('user_id')
    share_with_ids = request.form.getlist('share_with[]')

    # Save share entries in the DB
    for shared_id in share_with_ids:
        share = SavingsGoalShare(
            goal_id=None,  # Set None for non-goal tools
            shared_with_user_id=int(shared_id),
            tool_name='future_predictor',
            created_at=datetime.utcnow()
        )
        db.session.add(share)

    db.session.commit()
    flash("Future prediction shared successfully!", "success")
    return redirect(url_for('future_expense_predictor'))

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

# Route for expense splitter
@app.route('/expense-splitter', methods=['GET'])
@login_required_custom
def expense_splitter():
    user_id = session.get('user_id')

    # Fetch all expenses where the user is either the creator or a participant
    created_expenses = Expense.query.filter_by(creator_id=user_id).all()
    participant_expenses = ExpenseParticipant.query.filter_by(user_id=user_id).all()
    expense_ids = [p.expense_id for p in participant_expenses]
    participant_expenses = Expense.query.filter(Expense.id.in_(expense_ids)).all()

    # Combine both sets of expenses, avoiding duplicates
    expenses = list({exp.id: exp for exp in created_expenses + participant_expenses}.values())

    # Check if there are any expenses
    if not expenses:
        return redirect(url_for('create_expense'))

    # Select expense
    selected_expense_id = request.args.get("expense_id")
    selected_expense = None
    if selected_expense_id:
        selected_expense = next((exp for exp in expenses if exp.id == int(selected_expense_id)), None)

    # Fallback to the first expense if no valid selection
    if not selected_expense and expenses:
        selected_expense = expenses[0]

    # Fetch participants for the selected expense
    participants = []
    creator_name = ""
    my_payment = None

    if selected_expense:
        all_participants = ExpenseParticipant.query.filter_by(expense_id=selected_expense.id).all()
        for participant in all_participants:
            # Exclude the creator from the participants list
            if participant.user_id != user_id:
                participant.name = db.session.get(User, participant.user_id).name
                participants.append(participant)

        my_payment = ExpenseParticipant.query.filter_by(expense_id=selected_expense.id, user_id=user_id).first()
        if my_payment:
            my_payment.amount_paid = round(my_payment.amount_paid, 2)
            my_payment.amount_due = round(my_payment.amount_due, 2)
        else:
            my_payment = ExpenseParticipant(
            expense_id=selected_expense.id,
            user_id=user_id,
            amount_paid=0.0,
            amount_due=round(selected_expense.total_amount / (len(all_participants) + 1), 2),  # Including the creator
            status="Pending"
        )

        creator = db.session.get(User, selected_expense.creator_id)
        creator_name = creator.name if creator else ""

    return render_template(
        'expense_splitter.html',
        expenses=expenses,
        expense=selected_expense,
        participants=participants,
        creator_name=creator_name,
        my_payment=my_payment
    )

# Route for creating new expense
@app.route('/expense-splitter/create', methods=['GET', 'POST'])
@login_required_custom
def create_expense():
    user_id = session.get('user_id')

    if request.method == 'POST':
        try:
            # Get form data
            purpose = request.form.get('purpose', '')
            total_amount = float(request.form.get('total_expense') or 0.0)
            due_date_str = request.form.get('due_date', '')

            # Validate required fields
            if not purpose or total_amount <= 0:
                flash("Purpose and a valid Total Amount are required.", "danger")
                return redirect(url_for('create_expense'))

            # Parse the due date
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
                return redirect(url_for('create_expense'))

            # Get selected participant IDs from the form
            share_with_ids = request.form.getlist("share_with")

            # Calculate the amount per participant including creator
            num_participants = max(1, len(share_with_ids) + 1)
            amount_per_person = round(total_amount / num_participants, 2)

            # Create the new expense record
            expense = Expense(
                purpose=purpose,
                total_amount=total_amount,
                due_date=due_date,
                creator_id=user_id
            )
            db.session.add(expense)
            db.session.commit()

            # Add the creator as a participant
            creator_participant = ExpenseParticipant(
                expense_id=expense.id,
                user_id=user_id,
                amount_due=amount_per_person,
                amount_paid=0.0,
                status="Pending"
            )
            db.session.add(creator_participant)

            # Add each selected user as a participant
            for shared_id in share_with_ids:
                participant = ExpenseParticipant(
                    expense_id=expense.id,
                    user_id=int(shared_id),
                    amount_due=amount_per_person,
                    amount_paid=0.0,
                    status="Pending"
                )
                db.session.add(participant)

            # Commit all changes
            db.session.commit()
            flash("Expense created successfully!", "success")
            return redirect(url_for('expense_splitter', expense_id=expense.id))

        except Exception as e:
            flash(f"Error creating expense: {str(e)}", "danger")
            db.session.rollback()
            return redirect(url_for('create_expense'))

    # Get all users except the creator for participant selection
    users = User.query.filter(User.id != user_id).all()
    return render_template('create_expense.html', users=users)

# Route for editing expense
@app.route('/expense-splitter/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required_custom
def edit_expense(expense_id):
    try:
        user_id = session.get('user_id')
        expense = Expense.query.get(expense_id)

        if request.method == 'POST':
            # Get updated expense details from the form
            purpose = request.form.get("purpose")
            total_amount = float(request.form.get("total_expense") or 0.0)
            due_date = datetime.strptime(request.form.get("due_date"), '%Y-%m-%d').date()

            # Update the expense details
            expense.purpose = purpose
            expense.total_amount = total_amount
            expense.due_date = due_date

            # Delete existing participants
            ExpenseParticipant.query.filter_by(expense_id=expense_id).delete()

            # Get the list of selected participant IDs from the form
            share_with_ids = request.form.getlist("share_with")

            # Calculate the amount per participant including creator
            num_participants = max(1, len(share_with_ids) + 1)
            amount_per_person = round(total_amount / num_participants, 2)

            # Add the creator as a participant in the table
            creator_participant = ExpenseParticipant(
                expense_id=expense.id,
                user_id=user_id,
                amount_due=amount_per_person,
                amount_paid=0.0,
                status="Pending"
            )
            db.session.add(creator_participant)

            # Add each selected user as a participant
            for shared_id in share_with_ids:
                participant = ExpenseParticipant(
                    expense_id=expense.id,
                    user_id=int(shared_id),
                    amount_due=amount_per_person,
                    amount_paid=0.0,
                    status="Pending"
                )
                db.session.add(participant)

            db.session.commit()
            return redirect(url_for('expense_splitter', expense_id=expense.id))

        # List all users except the creator to display in the selection list
        users = User.query.filter(User.id != user_id).all()
        participants = ExpenseParticipant.query.filter_by(expense_id=expense.id).all()
        participant_ids = [p.user_id for p in participants]

        return render_template('edit_expense.html', expense=expense, users=users, participant_ids=participant_ids)

    except Exception as e:
        flash(f"Error editing expense: {str(e)}", "danger")
        db.session.rollback()
        return redirect(url_for('expense_splitter'))

# Route for deleting expense
@app.route('/expense-splitter/delete/<int:expense_id>', methods=['POST'])
@login_required_custom
def delete_expense(expense_id):
    try:
        expense = Expense.query.get(expense_id)
        if not expense:
            flash("Expense not found!", "danger")
            return redirect(url_for('expense_splitter'))

        # Delete related participants
        ExpenseParticipant.query.filter_by(expense_id=expense_id).delete()
        
        # Delete the expense itself
        db.session.delete(expense)
        db.session.commit()
        
        return redirect(url_for('expense_splitter'))
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting expense: {str(e)}", "danger")
        return redirect(url_for('expense_splitter'))

# Route for updating payment
@app.route('/expense-splitter/pay', methods=['POST'])
@login_required_custom
def update_payment():
    try:
        expense_id = int(request.form['expense_id'])
        amount_paid = float(request.form['amount'])
        user_id = session.get('user_id')

        participant = ExpenseParticipant.query.filter_by(expense_id=expense_id, user_id=user_id).first()
        if participant:
            # Validate the payment amount does not exceed the remaining amount
            remaining = max(participant.amount_due - participant.amount_paid, 0)
            if amount_paid > remaining:
                flash(f"Payment exceeds the remaining amount of ${remaining:.2f}.", "danger")
                return redirect(url_for('expense_splitter', expense_id=expense_id))

            # Update the paid amount
            participant.amount_paid += amount_paid

            # Recalculate the remaining amount after payment
            remaining = max(participant.amount_due - participant.amount_paid, 0)

            # Update status based on the remaining amount
            if remaining <= 0:
                participant.amount_paid = participant.amount_due  # Align paid amount with due amount
                participant.status = "Paid"
            elif participant.amount_paid > 0:
                participant.status = "Partial"
            else:
                participant.status = "Pending"

            db.session.commit()
            flash('Payment recorded successfully!', 'success')
            return redirect(url_for('expense_splitter', expense_id=expense_id))
        else:
            flash("No participant record found.", "danger")
    except Exception as e:
        db.session.rollback()
        flash(f"Error recording payment: {str(e)}", "danger")

    return redirect(url_for('expense_splitter', expense_id=expense_id))

@app.route('/share')
@login_required_custom
def share():
    user_id = session.get('user_id')

    # Shared by me: I'm the owner and have shared it with others
    shared_by_me = SavingsGoalShare.query.join(SavingsGoal).filter(SavingsGoal.user_id == user_id).all()

    # Shared with me: Others shared their goal with me
    shared_with_me = SavingsGoalShare.query.filter_by(shared_with_user_id=user_id).all()

    return render_template('share.html',
                           shared_by_me=shared_by_me,
                           shared_with_me=shared_with_me)

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Editing profile photo
@app.route('/upload-photo', methods=['POST'])
@login_required_custom
def upload_photo():
    if 'photo' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('profile'))

    file = request.files['photo']

    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('profile'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        user_id = session.get('user_id')

        # Save file to the upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{user_id}_{filename}")
        file.save(file_path)

        relative_path = f"media/uploads/{user_id}_{filename}"

        # Update user profile in the database
        profile = Profile.query.filter_by(user_id=user_id).first()
        if profile:
            profile.photo = relative_path
            db.session.commit()

        flash('Profile photo updated successfully!', 'success')
        return redirect(url_for('profile'))

    flash('Invalid file type. Please upload an image.', 'danger')
    return redirect(url_for('profile'))

@app.route('/delete-photo', methods=['POST'])
@login_required_custom
def delete_photo():
    user_id = session.get('user_id')

    try:
        # Find the user profile
        profile = Profile.query.filter_by(user_id=user_id).first()
        if profile:
            # Check if the photo is not default photo
            if profile.photo != 'media/images/user-review1.svg':

                file_name = os.path.basename(profile.photo)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                
                # Delete the photo from /uploads directory
                if os.path.exists(file_path):
                    os.remove(file_path)

            # Set the photo field to the default value
            profile.photo = 'media/images/user-review1.svg'

            db.session.commit()
            flash('Profile photo has been reset to the default image.', 'success')
        else:
            flash('User profile not found.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error while deleting photo: {str(e)}', 'danger')

    return redirect(url_for('profile'))


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

# Delete account from profile page
@app.route('/delete_account', methods=['POST'])
def delete_account():
    user_id = session.get('user_id')
    if not user_id:
        flash("You need to log in to delete your account.", "danger")
        return redirect(url_for('login'))

    try:
        # Delete user profile from user table
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)

        # Delete user from useProfile table
        profile = Profile.query.filter_by(user_id=user_id).first()
        if profile:
            db.session.delete(profile)

        # Delete user's budget plan from BudgetPlan table
        budget_plan = BudgetPlan.query.filter_by(user_id=user_id).first()
        if budget_plan:
            db.session.delete(budget_plan)

        # TODO: Add any table updated

        db.session.commit()
        # Clear session and logout
        session.clear()

        flash("Your account has been deleted successfully. See you again!", "success")
        return redirect(url_for('login'))

    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while deleting your account: {str(e)}", "danger")
        return redirect(url_for('profile'))

# API route to get EmailJS configuration
@app.route('/api/emailjs-config')
def get_emailjs_config():
    return jsonify({
        'serviceId': getenv('EMAILJS_SERVICE_ID'),
        'templateId': getenv('EMAILJS_TEMPLATE_ID'),
        'publicKey': getenv('EMAILJS_PUBLIC_KEY')
    })

if __name__ == '__main__':
    app.run(debug=True)
