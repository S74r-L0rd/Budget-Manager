from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your-very-secret-key'  # Replace with a strong secret in production

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
        session['user'] = 'harry@example.com'  # Simulate user login
        return redirect(url_for('dashboard'))  # Redirect to dashboard after login
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/share')
def share():
    return render_template('share.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
