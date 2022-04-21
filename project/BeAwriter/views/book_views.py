from flask import Blueprint, render_template, url_for, request, g, jsonify, current_app
from werkzeug.utils import redirect, secure_filename
import json
from gtts import gTTS 
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
                    book_title=temp,
                    #speaker_path=sb.book_con
                    )
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
                extension=f.filename.split('.')[-1]
                filename=f'{g.user.member_no}_{sb.book_no}.{extension}'
                f.save('../project/BeAwriter/static/image/'+ filename)              
                img = Image(book_no=sb.book_no,
                            img_path=filename)
                db.session.add(img)
                db.session.commit()

        if len(msg)==0 and msg1 is None:
            return redirect(url_for('book.readbook', book_no=book_no))
            
    return render_template('book/bookcover.html', msg=msg, msg1=msg1, book_no=book_no, isTitle=isTitle)

@bp.route('/bookstar/<int:book_no>', methods=('GET','POST'))
def bookstar(book_no):
    error = None
    
    if request.method == 'POST':
        try:
            VALUE = request.form['rating']
            star = Rating(member_no=g.user.member_no,
                          book_no=book_no,
                          rating=int(VALUE))
            db.session.add(star)
            db.session.commit()
            
        except:
            error = "평점을 매겨주세요!"
    
        if error is None:
            return redirect(url_for('main.index'))    
          
    return render_template("/book/bookstar.html", error=error, book_no=book_no)


@bp.route('/readbook/<int:book_no>/')
def readbook(book_no):
    book = Storybook.query.get_or_404(book_no)
    image = Image.query.get(book_no)
    content = book.book_con
    #audio_path = book.speak_path
    DIVN = [220, 320, 420, 520, 620]
    storyArray = []

    
    tts=gTTS(text=content, lang='ko')
    filename=str(g.user.member_no)+'_'+str(book.book_no)+'.mp3' #현재 동화책 제목으로 파일이름 지정하면될듯 f스트링으로 
    tts.save('../project/BeAwriter/static/'+filename)
    book.speak_path = filename
    db.session.commit()

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
    
    return render_template("/book/readbook.html", book=book, storyArray=storyArray, sa1=storyArray[1], sa2=storyArray[2], image=image,  book_no=book_no, audio_path=filename)
   


