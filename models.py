from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta

# Initialize the database
db = SQLAlchemy()




class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable = False)
    username = db.Column(db.String(128),unique = True,nullable = False)
    password=db.Column(db.String(128), nullable = False)
    books = db.relationship('Book', secondary='mybooks', backref='users')
    role = db.Column(db.String(64),nullable= False, default= False)

   

class Book(db.Model):
    __tablename__="book"
    id=db.Column(db.Integer,primary_key = True)
    title= db.Column(db.String(64), nullable = False)
    author=db.Column(db.String(64),nullable = False)
    date_created=db.Column(db.DateTime, nullable = False,default= datetime.now())
    description =db.Column(db.String(512), nullable = True)
    copies=db.Column(db.Integer,nullable=False)
    section_id = db.Column(db.Integer,db.ForeignKey('section.id'), nullable = True)
    blink = db.Column(db.String(64),nullable=False)
    book_feedback = db.relationship('Feedback', backref='books',lazy=True)
    sect = db.relationship('Section', backref=db.backref('books', lazy=True))

class Section(db.Model):
    __tablename__="section"
    id=db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),nullable =False)
    date_created=db.Column(db.DateTime, nullable = False,default= datetime.now())
    ebooks = db.relationship("Book", backref = "section", lazy = True)

class Mybooks(db.Model):
    __tablename__="mybooks"
    id=db.Column(db.Integer,primary_key= True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = True)
    book_id = db.Column(db.Integer,db.ForeignKey('book.id'), nullable = True)
    is_granted = db.Column(db.Boolean,nullable= False, default= False)
    issued_date = db.Column(db.DateTime, nullable = False, default= datetime.now())
    return_date = db.Column(db.DateTime, nullable = False,default= datetime.now() + timedelta(days=5))
    book = db.relationship('Book', backref='mybooks')
    user = db.relationship('User', backref='mybooks')
    access_requests = db.relationship('AccessRequests', backref='mybooks')
    feedback = db.relationship('Feedback', backref='mybooks')

class AccessRequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    ebook = db.Column(db.String(64), nullable=False)
    request_date = db.Column(db.DateTime, nullable=False,default= datetime.now())
    status = db.Column(db.String(20), nullable=False, default='Pending')
    mybooks_id = db.Column(db.Integer, db.ForeignKey('mybooks.id'), nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = True)
    book_id = db.Column(db.Integer,db.ForeignKey('book.id'), nullable = True)

class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer,db.ForeignKey('book.id'), nullable = False)
    content = db.Column(db.Text, nullable=True)
    mybooks_id = db.Column(db.Integer, db.ForeignKey('mybooks.id'), nullable=True)
    user = db.relationship('User', backref='feedback')
    book = db.relationship('Book', backref='feedback')

       
