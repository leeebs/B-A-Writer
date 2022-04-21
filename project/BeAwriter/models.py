from enum import unique
from pytz import timezone
from BeAwriter import db
from sqlalchemy.sql import func

class Member(db.Model):
    member_no = db.Column(db.Integer, primary_key=True, nullable=False)
    member_id = db.Column(db.String(20), nullable=False)
    member_password = db.Column(db.String(30), nullable=False)
    member_email = db.Column(db.String(30), nullable=False)
    member_name = db.Column(db.String(20), nullable=False)
    member_type = db.Column(db.SmallInteger, nullable=False, server_default='0')
    
class Storybook(db.Model):
    book_no = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    book_title = db.Column(db.String(50), nullable=False)
    book_con = db.Column(db.Text, nullable=False)
    book_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    member_no = db.Column(db.Integer,
                          db.ForeignKey('member.member_no', ondelete='CASCADE'),
                          nullable=False)
    
class Rating(db.Model):
    member_no = db.Column(db.Integer,
                          db.ForeignKey('member.member_no', ondelete='CASCADE'),
                          primary_key=True,
                          nullable=False)
    book_no = db.Column(db.Integer,
                        db.ForeignKey('storybook.book_no', ondelete='CASCADE'),
                        primary_key=True,
                        nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
class Image(db.Model):
    book_no = db.Column(db.Integer,
                        db.ForeignKey('storybook.book_no', ondelete='CASCADE'),
                        primary_key=True,
                        autoincrement=True,
                        nullable=False)
    img_path = db.Column(db.String(500), nullable=False)
    
class Question(db.Model):
    question_no = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    ques_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    member_no = db.Column(db.Integer,
                          db.ForeignKey('member.member_no', ondelete='CASCADE'),
                          nullable=False)
    member = db.relationship('Member', backref=db.backref("question"))                      
    
class QuestionComment(db.Model):
    comment_no = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    member_no = db.Column(db.Integer, db.ForeignKey('member.member_no', ondelete='CASCADE'), nullable=False)
    question_no = db.Column(db.Integer, db.ForeignKey('question.question_no', ondelete='CASCADE'), nullable=False)
    question = db.relationship('Question', backref=db.backref('questioncomment_set'))
    content = db.Column(db.String(200), nullable=False)
    comment_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)