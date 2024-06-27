from flask import Flask, render_template, redirect, url_for, request , session , g
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager , login_user , current_user , logout_user , UserMixin, login_required
from models import db, User , Section
from whoosh.analysis import StemmingAnalyzer
import flask_whooshalchemy






app = Flask(__name__)

# Configuration for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'somesecretkey'
app.config['WHOOSH_BASE'] = 'whoosh'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db.init_app(app)

# whooshalchemy.whoosh_index(app, Section)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @app.before_request
# def before_request_function():
#     users = User.query.all()
#     if 'user_id' in session:
#         user = [ x for x in users if x.email == session['user_id']]
#         if user :
#             g.user = user[0]
#         else:
#             g.user = None
#     else: 
#         g.user = None


    

@app.route('/')
@login_required
def home():
    if current_user.role == 'admin':
        return redirect(url_for('admindashboard'))
    return redirect(url_for('userdashboard'))
    # if g.user == None:
    #     print("we are redirecting to login page")
    #     return redirect(url_for('login'))
    # else:
    #     return redirect(url_for('userdashboard'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        u = User.query.filter_by(email=username).first()
        print(u)
        if u is not None and u.password == password:
            login_user(u)
            if u.role == 'admin':
                return redirect(url_for('admindashboard'))
            return redirect(url_for('userdashboard'))
        else:
            return render_template('wrongpassword.html', anyvariablename="Your Password is wrong.")
    else:
        return render_template('login.html')


@app.route('/userdashboard')
@login_required
def userdashboard():
    # if g.user == None:
    #     return redirect(url_for('login'))
    # print(session)
    print(current_user.id)
    cu = User.query.filter_by(id = current_user.id).first()
    sections = Section.query.all()
    name = cu.name
    return render_template('userdashboard.html' , name=name , sections = sections)

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
    logout_user()
    return "logout successfully."

@app.route('/admindashboard')
@login_required
def admindashboard():
    if current_user.role == 'admin':
        sections = Section.query.all()
        return render_template('adminpage.html' , sections=sections)
    else :
        return "Unauthorized Access"
    
@app.route('/section' , methods=['GET','POST'])
def create_section():
    if current_user.role =='admin':
        if request.method == 'POST':
            new_section = Section(name=request.form['name'])
            db.session.add(new_section)
            db.session.commit()
            return redirect(url_for('admindashboard'))
        return render_template('createnew-section.html')
    return "Unauthorized Access"

@app.route('/section/delete/<int:section_id>' , methods=["POST"])
def delete_section(section_id):
    section = Section.query.get(section_id)
    db.session.delete(section)
    db.session.commit()
    return redirect(url_for('admindashboard'))

@app.route('/section/update/<int:section_id>' , methods=["GET", "POST"])
def update_section(section_id):
    if request.method == "POST":
        section = Section.query.get(section_id)
        section.name = request.form['name']
        db.session.commit()
        return redirect(url_for('admindashboard'))
    else:
        section = Section.query.filter_by(id=section_id).first()
        return render_template('updatesection.html', section=section)


# @app.route('/sections')
# def get_all_sections():
#     return "all the books"


@app.route('/search' , methods=['POST'])
def search():
    if request.method == "POST":
        search_query = request.form['query']
        sections = Section.query.filter(Section.name.contains(search_query) | Section.id.contains(search_query)).all()
        cu = User.query.filter_by(id = current_user.id).first()
        name = cu.name
        return render_template('userdashboard.html', sections = sections , name = name)
    
@app.route('/search2' , methods=["POST"])
def search2():
        if request.method == "POST":
            search_query = request.form['query']
            sections = Section.query.whoosh_search(search_query).all()
            cu = User.query.filter_by(id = current_user.id).first()
            name = cu.name
        return render_template('userdashboard.html', sections = sections , name = name)

    

    






if __name__ == '__main__':
    if not os.path.exists('instance/mydatabase.db'):
        print("works")
        with app.app_context():
            db.create_all()
            admin_user = User(name = 'admin' , email = 'admin@gmail.com' , password = 'password' , role='admin')
            db.session.add(admin_user)
            db.session.commit()
    app.run()
