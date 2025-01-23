from flask import Flask, render_template, request, flash, redirect, url_for, Response
from functools import wraps
import logging
import os
import base64

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = "your-secret-key-here"  # Required for flash messages

# Basic Auth credentials
AUTH_USERNAME = "stanway"
AUTH_PASSWORD = "oscarhomework"

def check_auth(username, password):
    """Check if a username/password combination is valid."""
    return username == AUTH_USERNAME and password == AUTH_PASSWORD

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
@requires_auth
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        form_class = request.form.get('form', '').strip()

        # Validate inputs
        if not all([name, age, form_class]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('index'))

        try:
            age = int(age)
            if not (1 <= age <= 120):
                flash('Age must be between 1 and 120', 'error')
                return redirect(url_for('index'))
        except ValueError:
            flash('Please enter a valid age', 'error')
            return redirect(url_for('index'))

        # Save to file
        with open('data/submissions.txt', 'a') as f:
            f.write(f"Name: {name}, Age: {age}, Form: {form_class}\n")

        # Flash success message
        flash(f'Your name is {name}, you are {age} years old and in form {form_class}', 'success')
        return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/history')
@requires_auth
def history():
    submissions = []
    try:
        with open('data/submissions.txt', 'r') as f:
            submissions = f.readlines()
    except FileNotFoundError:
        pass
    return render_template('history.html', submissions=submissions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)