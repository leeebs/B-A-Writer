from flask import Blueprint, render_template, url_for, request, g, jsonify, session
from werkzeug.utils import redirect, secure_filename
import json

from BeAwriter import db
from BeAwriter.models import *

import speech_recognition as sr 
from gtts import gTTS 
import os 
import time
import playsound

bp = Blueprint('book', __name__, url_prefix='/book')

@bp.route('/', methods=('GET','POST'))
def make():
    msg = None
    
    if request.method == 'POST':
        content = request.form['writecontent']
        if not content:
            msg = "키워드나 짧은 문장을 작성해주세요!"
        if msg is None:
            return redirect(url_for('book.make')) #동화생성페이지로 수정
        
    return render_template('book/makebook.html', msg=msg)


@bp.route('/req', methods=['POST'])
def req():
    data = request.get_json()                 
    return jsonify(data)


@bp.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    sb = Storybook(book_con=data['alldata'],
                   member_no=g.user.member_no)
    db.session.add(sb)
    db.session.commit()
    bookn = { 'bookn' : sb.book_no }          
    return jsonify(bookn)


@bp.route('/cover/<int:book_no>/', methods=('GET','POST'))
def cover(book_no):
    msg = None       
    sb = Storybook.query.get(book_no)
    
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            msg = "파일을 넣고 제출 버튼을 눌러주세요."
        else:
            file_name = secure_filename(f.filename)
            f.save(file_name)
            img = Image(book_no=sb.book_no,
                        img_path=file_name)
            db.session.add(img)
            db.session.commit() 
            
        if msg is None:
            return redirect(url_for('main.index')) #동화읽는페이지로 수정
            
    return render_template('book/bookcover.html', msg=msg, book_no=book_no)

@bp.route('/bookstar/<int:book_no>/', methods=('GET','POST'))
def bookstar(book_no):
    sb = Storybook.query.get(book_no)
    if request.method == 'POST':
            request.form['rating']
            VALUE = request.form['rating']
            star = Rating(
                            member_no=g.user.member_no,
                            book_no=sb.book_no,
                            rating=int(VALUE))
            db.session.add(star)
            db.session.commit()
            return redirect(url_for('main.index'))

    return render_template("/book/bookstar.html")



@bp.route('/speaker')
def speaker():
    text = '안녕하세요 11조 화이팅'
    # tts=gTTS(text=text, lang='ko')
    # filename='voice.mp3'
    # tts.save(filename)
    return playsound.playsound(text)
    
@bp.route('/readbook')
def readbook():
    return render_template("/book/readbook.html")

@bp.route('/test')
def test():
    return render_template("test.html")