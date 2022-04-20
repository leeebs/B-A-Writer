from flask import Blueprint, render_template, url_for, request, g, jsonify
from werkzeug.utils import redirect, secure_filename
import json

from BeAwriter import db
from BeAwriter.models import *

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
    temp = "temp"
    if data['alldata']:
        sb = Storybook(book_con=data['alldata'],
                    member_no=g.user.member_no,
                    book_title=temp)
        db.session.add(sb)
        db.session.commit()
        book = { 'bookn' : sb.book_no,
                'con' : sb.book_con }   
    else:
        book = {}        
    return jsonify(book)


@bp.route('/cover/<int:book_no>/', methods=('GET','POST'))
def cover(book_no):
    msg1 = None
    msg = []  
    sb = Storybook.query.get(book_no)
    title = None
    isTitle = None
    if sb.book_title=="temp":
        isTitle = False
    else:
        isTitle = True

    if request.method == 'POST':
        if not isTitle and sb.book_title=="temp":
            title = request.form['title']
            if not title:
                msg1 = '제목을 입력해주세요!'
            else:
                sb.book_title = title
                db.session.commit()
                isTitle = True
                return render_template('book/bookcover.html', msg=msg, msg1=msg1, book_no=book_no, isTitle=isTitle)
        
        else:
            f = request.files['file']
            if not f:
                msg = ["파일을 넣고 제출 버튼을 눌러주세요.","생략 하시려면 생략하기 버튼을 눌러주세요."]
            else:
                file_name = secure_filename(f.filename)
                f.save(file_name)
                img = Image(book_no=sb.book_no,
                            img_path=file_name)
                db.session.add(img)
                db.session.commit()

        if len(msg)==0 and msg1 is None:
            return redirect(url_for('book.readbook', book_no=book_no)) #동화읽는페이지로 수정
            
    return render_template('book/bookcover.html', msg=msg, msg1=msg1, book_no=book_no, isTitle=isTitle)

@bp.route('/bookstar', methods=('GET','POST'))
def bookstar():
    error = None

    if request.method == 'POST':
        try:
            request.form['rating']
            VALUE = request.form['rating']
            star = Rating(rating_no=1,
                            member_no=2,
                            book_no=3,
                            rating=int(VALUE))
            db.session.add(star)
            db.session.commit()
            return redirect(url_for('main.index'))
        except: 
            error ="평점을 매겨주세요!"
         

          
    return render_template("/book/bookstar.html", error=error)


@bp.route('/readbook/<int:book_no>/')
def readbook(book_no):
    book = Storybook.query.get_or_404(book_no)
    
    content = book.book_con
    DIVN = [220, 320, 420, 520, 620]
    storyArray = []
    for divn in DIVN:
        story = []
        a = 0
        b = divn
        for _ in range(len(content)//divn):
            story.append(content[a:b])
            a += divn
            b += divn
        story.append(content[a:len(content)])
        storyArray.append(story)
    
    return render_template("/book/readbook.html", book=book, storyArray=storyArray, sa1=storyArray[1], sa2=storyArray[2])


