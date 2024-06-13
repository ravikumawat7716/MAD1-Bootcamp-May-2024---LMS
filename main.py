from flask import Flask
from flask import render_template
from flask import redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    print("we are redirecting to login page")
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/userdashboard')
def userdashboard():
    return "This is user dashboard"

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/admin-login')
def registe():
    return render_template('admin-login.html')


@app.route('/saurabh')
def somefunction():
    return render_template('index.html')





if __name__ == '__main__':
    app.run()