# Project Name: Budget-Manager

## 1. Project Introduction

Budget-Manager is a Flask-based web application designed to help users manage personal finances, track expenses, create budget plans, and set savings goals. It provides features such as user registration, login, expense recording, budget setting, consumption analysis, and includes automated UI testing using Selenium.

## 2. Main Features

### 2.1 User Registration (Sign Up)

- **Feature Description**: Allows new users to create an account by providing a username, email address, and password. The system verifies the validity of user input (e.g., password confirmation, email format, etc.) and stores user information in the database upon successful validation.

- **Related Files**: `app.py` (handling routes and logic), `models/user.py` (user data model), `templates/login.html` (registration form HTML template).

- **Testing Suggestions**: Unit tests and UI tests should be added for the user registration feature to verify:
  1. Whether registration with valid information completes successfully.
  2. Whether appropriate error messages are displayed when password and confirmation password don't match.
  3. Whether appropriate error messages are displayed when registering with an already registered email.
  4. Whether email format validation works properly.
  5. Whether password complexity requirements validation works properly.
  6. Whether users are correctly redirected to the login page or dashboard after successful registration.

### 2.2 User Login (Login)

- **Feature Description**: Allows registered users to log in by providing their email and password. The system verifies the correctness of the credentials, creates a user session upon successful login, and redirects to the user dashboard.

- **Related Files**: `app.py`, `login.py`, `models/user.py`, `templates/login.html` (login form HTML template).

- **Testing Suggestions**: Unit tests and UI tests should be added for the user login feature to verify:
  1. Whether registered users can successfully log in with correct credentials.
  2. Whether appropriate error messages are displayed when logging in with incorrect passwords.
  3. Whether appropriate error messages are displayed when logging in with non-existent emails.
  4. Whether users are correctly redirected to the dashboard after successful login.
  5. Whether sessions are correctly created and contain the necessary user information.
  6. Whether the "remember me" functionality works properly (if implemented).

### 2.3 Forgot Password (Forgot Password)

- **Feature Description**: (This feature is not explicitly shown in the provided test files, but if the project includes this feature, the typical workflow is as follows) Users who forget their password can click the "Forgot Password" link and enter their registered email address. The system sends an email containing a password reset link or verification code to that email. Users complete the password reset by following the instructions in the email.

- **Related Files**: If this feature exists, it might involve `app.py`, `emailVerification.py`, `models/user.py`, and corresponding HTML templates.

- **Testing Suggestions**: If the forgot password feature is implemented, appropriate unit tests and integration tests should be added to verify:
  1. Whether password reset emails are received after entering a valid email.
  2. The validity and time effectiveness of reset links or verification codes.
  3. Whether users can successfully set a new password through valid links/verification codes.
  4. Whether users can successfully log in using the new password.
  5. Handling of invalid or unregistered email inputs.

### 2.4 User Profile Management (Profile)

- **Feature Description**: Users can view and update personal information, such as name, contact information, personal preferences, etc.

- **Related Files**: `profile_update.py`, `models/userProfile.py`, `templates/profile.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the user profile management feature to verify:
  1. Whether users can correctly view their profile information.
  2. Whether updates to profile information are correctly saved to the database.
  3. Whether form validation works properly (e.g., phone format, postal code, etc.).
  4. Whether modifications to sensitive information require secondary verification (e.g., password verification when modifying email).
  5. Whether the avatar upload functionality works properly (if implemented).
  6. Whether view and edit permission controls are correct (ensuring users can only view and edit their own profiles).

## 3. Core Financial Management Features

### 3.1 Dashboard (Dashboard)

- **Feature Description**: A personal financial overview page displaying recent expenses, budget status, savings goal progress, and other key information.

- **Related Files**: `app.py`, `templates/dashboard.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the dashboard feature to verify:
  1. Whether the dashboard displays correct user data (amounts, percentages, etc.).
  2. Whether data visualization charts render correctly.
  3. Whether the dashboard is responsive and adapts to different screen sizes.
  4. Whether dashboard data updates in real-time based on the user's latest financial activities.
  5. Testing dashboard display states under different scenarios (no expense records, budget overspending, approaching savings goals, etc.).
  6. Whether various conversion rates and summary calculations are accurate.

### 3.2 Expense Tracking (Expense Tracker)

- **Feature Description**: Allows users to record, categorize, and view personal expenses. Users can add new expense records and view historical expense data.

- **Related Files**: `models/Expense.py`, `templates/expense_tracker.html`, `templates/create_expense.html`, `templates/edit_expense.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the expense tracking feature to verify:
  1. Whether historical expense records are displayed correctly.
  2. Whether pagination functionality works properly (if implemented).
  3. Whether filtering and sorting functionalities are effective (by date, amount, category, etc.).
  4. Whether summary data (total expenses, average expenses, etc.) is calculated accurately.
  5. Whether export functionality works properly (if implemented).
  6. In a multi-user environment, ensuring users can only see their own expense records.

### 3.3 Create Expense (Create Expense)

- **Feature Description**: Provides an interface for users to input new expense information, including amount, category, date, description, etc., and saves the data to the database.

- **Related Files**: `models/Expense.py`, `templates/create_expense.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the create expense feature to verify:
  1. Whether form validation works properly (required fields, amount format, etc.).
  2. Whether expense records are successfully created after submitting valid data.
  3. Whether the date picker functionality works properly.
  4. Whether the category selection includes all predefined categories.
  5. Whether custom category addition functionality works properly (if implemented).
  6. Whether appropriate redirection or success messages are displayed after successful expense record creation.
  7. Whether receipt image upload functionality works properly (if implemented).

### 3.4 Edit Expense (Edit Expense)

- **Feature Description**: Allows users to modify existing expense record information, such as updating amount, changing category, or adding/modifying descriptions.

- **Related Files**: `models/Expense.py`, `templates/edit_expense.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the edit expense feature to verify:
  1. Whether existing expense data is correctly loaded into the edit form.
  2. Whether modified data is correctly saved to the database.
  3. Whether form validation works properly.
  4. Whether users can only edit their own expense records.
  5. Whether cancel edit functionality works properly.
  6. Whether edit history is recorded (if audit trail functionality is implemented).

### 3.5 Budget Planning (Budget Planner)

- **Feature Description**: Users can set budgets for different categories on a monthly or weekly basis, and the system tracks actual expenses against the budget.

- **Related Files**: `models/budgetPlan.py`, `templates/budget_planner.html`, `templates/edit_budget.html`, `templates/budget_saved_success.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the budget planning feature to verify:
  1. Whether creating new budget plans functionality works properly.
  2. Whether budget settings for different time periods (weekly, monthly, quarterly, etc.) are correctly saved.
  3. Whether the comparison calculation between budget and actual expenses is accurate.
  4. Whether budget overspending warnings are triggered properly (if implemented).
  5. Whether budget charts and visualizations are displayed correctly.
  6. Whether copying previous period's budget functionality works properly (if implemented).
  7. In a multi-user environment, ensuring users can only view and edit their own budget plans.

### 3.6 Edit Budget (Edit Budget)

- **Feature Description**: Allows users to modify existing budget plans, such as adjusting budget amounts, changing time ranges, or modifying budget categories.

- **Related Files**: `models/budgetPlan.py`, `templates/edit_budget.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the edit budget feature to verify:
  1. Whether existing budget data is correctly loaded into the edit form.
  2. Whether modified budgets are correctly saved to the database.
  3. Whether form validation works properly.
  4. Whether addition, deletion, or modification of budget categories is handled correctly.
  5. Whether changes to budget periods are handled correctly.
  6. Whether users can only edit their own budget plans.

### 3.7 Savings Goal Tracking (Savings Goal Tracker)

- **Feature Description**: Users can set savings goals (such as vacations, purchasing large items, etc.) and track goal completion progress.

- **Related Files**: `models/savings_goal.py`, `templates/savings_goal_tracker.html`, `templates/edit_goal.html`, `templates/savings_goal_success.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the savings goal tracking feature to verify:
  1. Whether creating new savings goals functionality works properly.
  2. Whether progress calculation is accurate (comparison between saved amount and target amount).
  3. Whether goal achievement rate and expected completion date calculations are correct.
  4. Whether notifications or markers are properly displayed after goals are completed.
  5. Whether management and sorting of multiple goals works properly.
  6. Whether adding savings record functionality works properly.
  7. In a multi-user environment, ensuring users can only view and edit their own savings goals.

### 3.8 Edit Savings Goal (Edit Savings Goal)

- **Feature Description**: Provides an interface for users to modify existing savings goals, including target amount, completion date, goal description, and other information.

- **Related Files**: `models/savings_goal.py`, `templates/edit_goal.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the edit savings goal feature to verify:
  1. Whether existing goal data is correctly loaded into the edit form.
  2. Whether modified goal information is correctly saved to the database.
  3. Whether progress calculation updates appropriately after increasing or decreasing the target amount.
  4. Whether expected completion status calculation is correct after deadline modification.
  5. Whether goal cancellation or completion marking functionality works properly.
  6. Whether users can only edit their own savings goals.

## 4. Advanced Features and Analysis Tools

### 4.1 Expense Analysis (Expense Analysis)

- **Feature Description**: Provides visualization analysis of expense data, such as expense charts by category and time period, helping users understand spending patterns.

- **Related Files**: `templates/analysis.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the expense analysis feature to verify:
  1. Whether various charts (pie charts, bar charts, line charts, etc.) render correctly.
  2. Whether data calculations and summaries are accurate.
  3. Whether time range filtering (this week, this month, this year, etc.) works properly.
  4. Whether category filtering and comparison functionalities are effective.
  5. Whether export analysis report functionality works properly (if implemented).
  6. Performance and response speed with large datasets.
  7. Whether chart interaction functionalities (hover display details, zoom, etc.) work properly.

### 4.2 Spending Personality Analyzer (Spending Personality Analyzer)

- **Feature Description**: Analyzes users' spending personality types based on spending habits and patterns, and provides corresponding financial advice.

- **Related Files**: `spending_personality_analyzer.py`, `templates/spending_personality_analyzer.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the spending personality analyzer feature to verify:
  1. Whether the analysis algorithm works based on sufficient data samples (e.g., at least one month of transaction records).
  2. Whether different personality analysis results can be derived from different spending patterns.
  3. Whether the financial advice provided matches the analysis results.
  4. Whether user feedback mechanisms work properly (if implemented).
  5. Whether analysis results update with changes in time and spending habits.
  6. Whether comparison and benchmark testing functionalities are correct (comparison with similar groups, etc.).
  7. Sensitivity testing: whether small spending changes cause large personality type changes.

### 4.3 Future Expense Predictor (Future Expense Predictor)

- **Feature Description**: Uses historical expense data and trend analysis to predict users' possible future expenses, helping users better plan their finances.

- **Related Files**: `models/my_prediction.py`, `models/future_prediction_share.py`, `templates/future_expense_predictor.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the future expense predictor feature to verify:
  1. Whether the prediction algorithm can produce reasonable prediction results when there is sufficient historical data.
  2. Whether the visualization of prediction results is clear and easy to understand.
  3. Whether predictions for different time spans (next month, next quarter, next year) are available.
  4. Whether seasonal spending patterns are correctly identified and predicted.
  5. Whether abnormal expenses are excluded from the prediction basis.
  6. Whether users can adjust prediction parameters (if implemented).
  7. Whether feedback mechanisms exist and are effective for comparing predictions with actual expenses.

## 5. Collaboration and Sharing Features

### 5.1 Expense Splitter (Expense Splitter)

- **Feature Description**: Allows users to record and manage expenses shared with others, such as team dinners, house rentals, etc., and calculates the amount each person should share.

- **Related Files**: `models/ExpenseParticipant.py`, `templates/expense_splitter.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the expense splitter feature to verify:
  1. Whether adding participants for expense splitting functionality works properly.
  2. Whether average splitting and custom splitting ratio calculations are accurate.
  3. Whether different splitting methods (equal amounts, proportional, by consumption items) are correctly implemented.
  4. Whether settlement status tracking is correct (paid, unpaid, etc.).
  5. Whether sending reminders or invitation functionality works properly (if implemented).
  6. Whether multi-currency support and exchange rate conversion are correct (if implemented).
  7. Whether shared expense history records and summary reports are available.

### 5.2 Financial Information Sharing (Financial Sharing)

- **Feature Description**: Users can selectively share their budget plans, savings goals, or expense predictions with others, facilitating collaborative financial management or obtaining advice.

- **Related Files**: `models/savings_goal_share.py`, `models/future_prediction_share.py`, `templates/share.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the financial information sharing feature to verify:
  1. Whether sharing link generation and access control work properly.
  2. Whether permission level settings for sharing are effective (read-only, can comment, can edit, etc.).
  3. Whether the selection and limitation of sharing targets work properly.
  4. Whether share revocation and expiration mechanisms are effective.
  5. Whether comment or suggestion functionality for shared content works properly.
  6. Whether sharing history records and notification functionalities are available.
  7. Whether privacy protection measures are adequate (blurring of sensitive information, etc.).

## 6. Auxiliary Features

### 6.1 Contact Support (Contact Support)

- **Feature Description**: Users can contact the application support team through this page, provide feedback on issues, or make suggestions.

- **Related Files**: `templates/contact.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the contact support feature to verify:
  1. Whether contact form submission works properly.
  2. Whether required field validation is effective.
  3. Whether email sending functionality is correctly configured and works.
  4. Whether file upload functionality works properly (if implemented).
  5. Whether the automatic reply system is configured and works.
  6. Whether user submission history is recorded and accessible.
  7. Whether anti-spam measures for forms are effective (such as CAPTCHA).

### 6.2 Tools Collection (Tools)

- **Feature Description**: Provides a series of practical financial tools, such as loan calculators, interest rate comparison tools, etc.

- **Related Files**: `templates/tools.html`

- **Testing Suggestions**: Unit tests and UI tests should be added for the tools collection feature to verify:
  1. Whether the calculation logic of various calculators is accurate.
  2. Whether input validation is effective (preventing non-numeric inputs, etc.).
  3. Whether calculation result visualization is clear.
  4. Whether result saving or export functionality works properly (if implemented).
  5. Whether advanced options and parameter adjustments correctly affect calculation results.
  6. Usability and responsive design on mobile devices.
  7. Whether integration between tools is smooth (output from one tool to another).

### 6.3 Data Import/Export (Data Import/Export)

- **Feature Description**: Supports users importing expense data in spreadsheet format, or exporting their financial data for backup or further analysis.

- **Related Files**: `templates/expense_template.xlsx`

- **Testing Suggestions**: Unit tests and UI tests should be added for the data import/export feature to verify:
  1. Whether supported file formats and import templates are correctly recognized.
  2. Whether the data validation mechanism can identify and handle imported data that does not conform to specifications.
  3. Performance and error handling for importing large amounts of data.
  4. Whether the export functionality can generate complete data in the proper format.
  5. Whether different export format options are available (CSV, Excel, PDF, etc.).
  6. Whether selective export functionality works properly (filtering by date range, category, etc.).
  7. Whether import/export history records are saved and accessible.

## 7. Testing Instructions

### 7.1 Environment Setup

1.  **Python Environment**: Ensure Python is installed (recommended version 3.8+).
2.  **Create Virtual Environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate   # Windows
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    `requirements.txt` should include Flask, Flask-SQLAlchemy, Flask-Testing, Selenium, Werkzeug, and other necessary libraries. According to `loginSeleniumTest.py`, Chrome browser and corresponding ChromeDriver also need to be installed.
    *   **ChromeDriver**: You need to download the ChromeDriver that corresponds to your installed Chrome browser version, and configure its path in the system environment variable `PATH`, or specify its path in the Selenium code.

4.  **Database Initialization**:
    Tests typically run on an independent test database, or tables are created before each test and destroyed after the test. `BaseTestCase` in `testConfig.py` includes `db.create_all()` and `db.drop_all()`, indicating that tests will automatically handle database creation and cleanup.

### 7.2 Test Execution Commands

In the project root directory, open a terminal and activate the virtual environment, then you can use the following command to run all tests:

```bash
python3 -m unittest discover test
```

Or run tests for specific files:

```bash
python3 -m unittest test.loginTest
python3 -m unittest test.loginSeleniumTest
```

### 7.3 Unit Tests (`test/loginTest.py`)

This file uses the Flask-Testing framework to perform unit tests on user registration and login functionality.

-   **Test Registration (`test_register`)**:
    -   Simulate user registration form submission through `self.client.post('/register', ...)`.
    -   Assert whether the response status code is 200 (success).
    -   Assert whether the response content includes "registration successful" prompt information.
-   **Test Login (`test_login`)**:
    -   First, register a test user through API call.
    -   Then, simulate user login form submission through `self.client.post('/login', ...)`.
    -   Assert whether the response status code is 200.
    -   Assert whether the page content after successful login includes "dashboard" (usually the target page to jump to after login).
-   **Test Invalid Credentials Login (`test_login_invalid_credentials`)**:
    -   Simulate user login with incorrect email and password.
    -   Assert whether the response status code is 200 (because usually login failure also returns 200, but displays error information on the page).
    -   Assert whether the response content includes "login failed" prompt information.

These tests do not involve browser operations and directly test backend logic and responses.

### 7.4 Selenium UI Tests (`test/loginSeleniumTest.py`)

This file uses Selenium WebDriver to perform end-to-end (E2E) or UI tests on user registration and login functionality. This means the tests will simulate real user operations in the browser.

-   **Environment Setup (`setUpClass`, `run_flask_server`, `setUp`, `tearDown`)**:
    -   `setUpClass`: Before all tests start, start a background thread to run the Flask application. This is necessary because Selenium needs a running web server to interact with.
    -   `run_flask_server`: The function that actually runs the Flask application.
    -   `setUp`: Executed before each test method:
        -   Call the parent class's `setUp` (i.e., `BaseTestCase.setUp()`, which executes `db.create_all()`).
        -   Initialize Chrome WebDriver (set to headless mode, not showing the browser interface).
    -   `tearDown`: Executed after each test method:
        -   Close WebDriver.
        -   Call the parent class's `tearDown` (i.e., `BaseTestCase.tearDown()`, which executes `db.drop_all()`).

-   **Test User Registration (`test_1_register`)**:
    1.  Open the login page (`http://127.0.0.1:5000/login`).
    2.  Switch to the registration tab.
    3.  Fill in username, email, password, and confirmation password in the form.
    4.  Check the agree to terms checkbox.
    5.  Click the submit button.
    6.  Wait and verify whether "registration successful" success message appears on the page.

-   **Test Registered User Login (`test_2_login_registered_user`)**:
    1.  **Pre-register User**: To ensure test independence and database cleanliness, this test first registers a user directly in the current test database through API (`self.client.post('/register', ...)`). This is because `setUp` and `tearDown` clean and rebuild the database for each test, so the user created by the previous `test_1_register` is not available here.
    2.  **UI Login**:
        -   Open the login page.
        -   Fill in the registered user's email and password.
        -   Click the submit button.
        -   Wait and verify whether the URL includes "dashboard", indicating successful redirection.

-   **Test Invalid Credentials Login (`test_3_login_invalid_credentials`)**:
    1.  Open the login page.
    2.  Fill in incorrect email and password.
    3.  Click the submit button.
    4.  Wait and verify whether "login failed" error message appears on the page.

These Selenium tests ensure that user interface interactions meet expectations and are important means to verify user experience and front-end back-end integration.

## 8. Notes
- Ensure the `requirements.txt` file is up to date and includes all dependencies required for running and testing the project.
- The ChromeDriver version must match the Chrome browser version installed on your system.
- Before running Selenium tests, ensure no other services are occupying the port that the Flask application will use (default is 5000).

## 9. Project Installation and Running Guide

### 9.1 System Requirements
- Python 3.8 or higher
- Chrome browser (for running Selenium tests)
- Corresponding version of ChromeDriver
- Git (for cloning the project)

### 9.2 Get Project Code
```bash
# Clone the project repository
git clone <Project Git URL>
# Enter the project directory
cd Budget-Manager
```

### 9.3 Environment Configuration
1. **Create Virtual Environment**:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (select command based on operating system)
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

2. **Install Dependencies**:
```bash
# Install all required dependency packages
pip install -r requirements.txt
```

3. **Database Initialization**:
```bash
# Initialize database and apply migrations
flask db upgrade
```

### 9.4 Run Project
```bash
# Start Flask application
flask run
```
The application will run at http://127.0.0.1:5000/, which can be accessed through a browser.

### 9.5 Install Additional Dependencies for Testing

1. **ChromeDriver Installation**:
   - Download the ChromeDriver matching your Chrome browser version: [ChromeDriver Download Page](https://sites.google.com/a/chromium.org/chromedriver/downloads)
   - Extract the downloaded file
   - Add ChromeDriver to the system PATH environment variable:
     - **Linux/macOS**:
       ```bash
       # Move to executable directory
       sudo mv chromedriver /usr/local/bin/
       # Set execution permission
       sudo chmod +x /usr/local/bin/chromedriver
       ```
     - **Windows**:
       - Place ChromeDriver.exe in any directory included in the PATH environment variable, or
       - Add the ChromeDriver path to the system's PATH environment variable

2. **Test Dependency Confirmation**:
   ```bash
   # Ensure all libraries required for testing are installed
   pip install -r requirements.txt
   ```

### 9.6 Run Tests
See the "7.2 Test Execution Commands" section above for instructions.
