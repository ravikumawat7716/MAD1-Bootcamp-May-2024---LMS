from flask import Flask, render_template, redirect, url_for, request
import os
from models import db, User, Book, Section, Mybooks, AccessRequests, Feedback

app = Flask(__name__)

# Configuration for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


@app.route('/')
def home():
    print("we are redirecting to login page")
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        # Add logic to check username and password
        # For demonstration purposes, let's assume the login is always successful
        # You should add actual logic to validate the username and password
        print(username)
        print(password)
        if username and password:  # Replace with actual validation
            return render_template('userdashboard.html', name=username)
        else:
            return render_template('wrongpassword.html', anyvariablename="Password")
    return render_template('login.html')

@app.route('/userdashboard')
def userdashboard():
    return "This is user dashboard"

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/admin-login')
def admin_login():
    return render_template('admin-login.html')

@app.route('/saurabh')
def somefunction():
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('instance/mydatabase.db'):
        print("works")
        with app.app_context():
            db.create_all()  # This will create the tables if the database does not exist
    app.run()
