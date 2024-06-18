from flask import Flask, render_template, redirect, url_for, request , session , g
from flask_sqlalchemy import SQLAlchemy
import os

from models import db, User

app = Flask(__name__)

# Configuration for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'somesecretkey'


db.init_app(app)


@app.before_request
def before_request_function():
    users = User.query.all()
    if 'user_id' in session:
        user = [ x for x in users if x.email == session['user_id']]
        if user :
            g.user = user[0]
        else:
            g.user = None
    else: 
        g.user = None
    

@app.route('/')
def home():
    if g.user == None:
        print("we are redirecting to login page")
        return redirect(url_for('login'))
    else:
        return redirect(url_for('userdashboard'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        u = User.query.filter_by(email=username).first()
        if u.password == password:
            session['user_id'] = username
            # return render_template('userdashboard.html', name=username)
            return redirect(url_for('userdashboard'))
        else:
            return render_template('wrongpassword.html', anyvariablename="Your Password is wrong.")
    else:
        return render_template('login.html')


@app.route('/userdashboard')
def userdashboard():
    if g.user == None:
        return redirect(url_for('login'))
    print(session)
    return "this is the user dashbard"

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        userrole = "user"
        new_user = User(name = name , email = email , password = password , role=userrole)
        db.session.add(new_user)
        db.session.commit()
        return "Data Saved Successfully."
    return render_template('register.html')

@app.route('/admin-login')
def admin_login():
    return render_template('admin-login.html')

@app.route('/saurabh')
def somefunction():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return "logout successfully."

if __name__ == '__main__':
    if not os.path.exists('instance/mydatabase.db'):
        print("works")
        with app.app_context():
            db.create_all()  # This will create the tables if the database does not exist
    app.run()
