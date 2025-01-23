from flask import Flask, render_template, request, flash, redirect, url_for
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = "your-secret-key-here"  # Required for flash messages

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        form_class = request.form.get('form')
        
        # Save to file
        with open('data/submissions.txt', 'a') as f:
            f.write(f"Name: {name}, Age: {age}, Form: {form_class}\n")
        
        # Flash success message
        flash(f'Your name is {name}, you are {age} years old and in form {form_class}', 'success')
        return redirect(url_for('index'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
