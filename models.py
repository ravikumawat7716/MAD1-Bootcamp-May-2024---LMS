from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(128), nullable=False)
    date_created = db.Column(db.DateTime , nullable=False , default=datetime.now())

# class Section(db.Model):
#     __tablename__="section"
#     id=db.Column(db.Integer,primary_key = True)
#     name = db.Column(db.String(64),nullable =False)
#     date_created=db.Column(db.DateTime, nullable = False,default= datetime.now())
#     ebooks = db.relationship("Book", backref = "section", lazy = True)

# class Book(db.Model):
#     __tablename__="book"
#     id=db.Column(db.Integer,primary_key = True)
#     title= db.Column(db.String(64), nullable = False)
#     author=db.Column(db.String(64),nullable = False)
#     date_created=db.Column(db.DateTime, nullable = False,default= datetime.now())
#     description =db.Column(db.String(512), nullable = True)
#     copies=db.Column(db.Integer,nullable=False)
#     section_id = db.Column(db.Integer,db.ForeignKey('section.id'), nullable = True)
#     blink = db.Column(db.String(64),nullable=False)
#     book_feedback = db.relationship('Feedback', backref='books',lazy=True)
#     sect = db.relationship('Section', backref=db.backref('books', lazy=True))