# Project Name: Budget-Manager

## Group Members

| UWA ID    | Name                         | GitHub Username        |
|-----------|------------------------------|------------------------|
| 24038357  | Iliyas Akhmet                | ilikmeister            |
| 23746416  | Chaewon Seo                  | febius47 / Chaewon Seo |
| 24525791  | Aakash Kozhukkunnon Othayoth | S74r-L0rd              |
| 22794111  | Ying Hu                      | Minanow                |

## 1. Project Introduction

Budget-Manager is a Flask-based web application designed to help users manage personal finances, track expenses, create budget plans, set savings goals, predict future expense, analyze spending personality, and record shared expenses. It provides features such as user registration, login, update profile, sharing analyzed data between users and includes automated UI testing using Selenium. 

## 2. Main Features for visitors

### 2.1 Home page 

Feature Description:  It shows overall description of our web page, including what we provide and it shows the reviews from our users. It also shows the Privacy policy and how we make our user’s data in compliance to our Privacy policy. 

### 2.2  Tools page 

Feature Description: It shows the catalogue of tools that we provide to do the financial analysis in the Guest View before user login. Also, provides brief guidance of how to use the tools and why to use our tools. 

### 2.3 Contact Support 

Feature Description: Users can contact the application support team through this page, provide feedback on issues, or make suggestions. 


## 3. Main Features for users 
### 3.1 User Registration (Sign Up) 

Feature Description: Allows new users to create an account by providing a username, email address, and password. The system verifies the validity of user input (e.g., password confirmation, email format, etc.) and stores user information in the database upon successful validation.

### 3.2 User Login (Login) 

Feature Description: Allows registered users to log in by providing their email and password. The system verifies the correctness of the credentials, creates a user session upon successful login, and redirects to the user dashboard. 

### 3.3 Forgot Password (Forgot Password) 

Feature Description: (This feature is not explicitly shown in the provided test files, but if the project includes this feature, the typical workflow is as follows) Users who forget their password can click the "Forgot Password" link and enter their registered email address. The system sends an email containing a password reset link or verification code to that email. Users complete the password reset by following the instructions in the email. 

### 3.4 Profile page 

Feature Description: Users can view and update personal information, such as name, contact information, personal preferences, etc.Users can view and update personal information, such as name, contact information, occupation, etc. Users will be able to upload and delete profile photos. Also, users will be able to update their password and delete the account from profile page. 
 
### 3.5 Dashboard 

Feature Description: A personal financial overview page displaying recent expenses, budget status, savings goal progress, and other key information. 

### 3.6 Analysis page 

Feature Description: It shows the catalogue of tools that we provide to do the financial analysis in the User View after user login. It is the landing page to navigate to any of the tools for its usage. 

### 3.7 Sharing Hub page 

Feature Description: It shows the data which was shared by the user and the data which was received to the user. This shows the details regarding the report summary that was shared, the tools which was used to generate the report, shared date and a view button to view the report from its respective tools page. 

 
## 4. Analysing Tools 

### 4.1 Expense Tracker 

Feature Description: It allows users to see and track their expenses categorically, helping them in understanding where exactly they spent more. 

### 4.2 Budget Planner 

Feature Description: Users can set budgets for different categories on a yearly, monthly, weekly or daily basis, and the system tracks actual expenses against the budget. 

### 4.3 Savings Goal Tracker 

Feature Description: Users can set savings goals (such as vacations, purchasing house or a car, etc.) and track goal completion progress. The user can share the goals created specifically to other users of their choice. The other user will receive the shared goal, and he can review it. 

### 4.4 Spending Personality Analyzer 

Feature Description: Analyses users' spending personality types based on user's spendings data. The tool will compare the spending trend with the user’s group average and show bar charts. Users can share their personality results with other users. 

## 4.5 Future Expense Predictor 

Feature Description: Uses historical expense data and trend analysis to predict users' possible future expenses, helping users better plan their finances. The user can also share his predicted report and their top predictions to other users of their own choice. The other user will receive the report, and he can review it. 

### 4.6 Expense Splitter 

Feature Description: Allows users to record and manage expenses shared with others, such as team dinners, house rentals, etc., and calculates the amount each person should share. Users will be able to record their payments and check the remaining. Users can create and edit expenses. 

## 5. Testing Instructions

### 5.1 Environment Setup

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

### 5.2 Test Execution Commands

In the project root directory, open a terminal and activate the virtual environment, then you can use the following command to run all tests:

```bash
python3 -m unittest discover test
```

Or run tests for specific files:

```bash
python3 -m unittest test.loginTest
python3 -m unittest test.loginSeleniumTest
```

### 5.3 Unit Tests (`test/loginTest.py`)

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

### 5.4 Selenium UI Tests (`test/loginSeleniumTest.py`)

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

## 6. Notes
- Ensure the `requirements.txt` file is up to date and includes all dependencies required for running and testing the project.
- The ChromeDriver version must match the Chrome browser version installed on your system.
- Before running Selenium tests, ensure no other services are occupying the port that the Flask application will use (default is 5000).

## 7. Project Installation and Running Guide

### 7.1 System Requirements
- Python 3.8 or higher
- Chrome browser (for running Selenium tests)
- Corresponding version of ChromeDriver
- Git (for cloning the project)

### 7.2 Get Project Code
```bash
# Clone the project repository
git clone <Project Git URL>
# Enter the project directory
cd Budget-Manager
```

### 7.3 Environment Configuration
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

### 7.4 Run Project
```bash
# Start Flask application
flask run
```
The application will run at http://127.0.0.1:5000/, which can be accessed through a browser.

### 7.5 Install Additional Dependencies for Testing

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

### 7.6 Run Tests
See the "7.2 Test Execution Commands" section above for instructions.


## 9.Reference

In the development of this project, we have utilised Generative AI tools to enhance code generation and problem-solving. The following AI tools were utilised:

GitHub Copilot: Utilised for code completion in vscode, detecting syntax error and in-file code related queries.
ChatGPT 4.0: Utilised for problem solving questions and general technology related questions. Also, utilised for code generation and design suggestions.
Claude: Utilised for code revision and queries.

These tools were employed for our advanced web development.
