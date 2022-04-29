from flask import Blueprint, render_template, url_for, request, g, jsonify, current_app
from werkzeug.utils import redirect, secure_filename
import json
from gtts import gTTS 
from BeAwriter import db
from BeAwriter.models import *
from datetime import datetime
from sqlalchemy import and_

from transformers import AutoModelWithLMHead, PreTrainedTokenizerFast
from fastai.text.all import *
from hanspell import spell_checker
import re

def preprocessing(res):
    spelled_sent = spell_checker.check(res)
    hanspell_sent = spelled_sent.checked
    return hanspell_sent

def outputmodel(input):
    PATH = "../project/BeAwriter/static/storymodel/"
    model = AutoModelWithLMHead.from_pretrained(PATH)
    tokenizer = PreTrainedTokenizerFast.from_pretrained(PATH)
    
    device = "cpu"
    model = model.to(device)

    prompt_ids = tokenizer.encode(input)
    inp = tensor(prompt_ids)[None].cpu()
    preds = model.generate(inp,
                            use_cache=True,
                            pad_token_id=tokenizer.pad_token_id,
                            eos_token_id=tokenizer.eos_token_id,
                            bos_token_id=tokenizer.bos_token_id,
                            max_length=30,
                            do_sample=True,
                            repetition_penalty=5.0,
                            temperature=0.9,
                            top_k=50,
                            top_p=0.92
                        ) 
    output = tokenizer.decode(preds[0].cpu().numpy())
    output = re.sub('[0-9:\n]','',output)
    return output


bp = Blueprint('book', __name__, url_prefix='/book')

@bp.route('/', methods=('GET','POST'))
def make():
    msg = None
    
    if request.method == 'POST':
        content = request.form['writecontent']
        if not content:
            msg = "키워드나 짧은 문장을 작성해주세요!"
        # else:
        #     hanspell_sent = preprocessing(content)
        #     res = outputmodel(hanspell_sent)
        #     res = preprocessing(res)
        #     return res
        
        if msg is None:
            return render_template('book/makebook.html')
        
    return render_template('book/makebook.html', msg=msg)


@bp.route('/req', methods=['POST'])
def req():
    data = request.get_json()                 
    return jsonify(data)

@bp.route('/req_story', methods=['POST'])
def req_story():
    data = request.get_json()
    if data['inputdata']:
        hanspell_sent = preprocessing(data['inputdata'])
        res = outputmodel(hanspell_sent)
        outputdata = preprocessing(res)
        output = { 'outputdata' : outputdata }
    else:
        output = {}        
    return jsonify(output)                

@bp.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    temp = "temp"
    if data['alldata']:
        sb = Storybook(book_con=data['alldata'],
                    member_no=g.user.member_no,
                    book_title=temp,
                    book_date = datetime.now(timezone('Asia/Seoul')))
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
    book = None
    isIt = None
    
    if request.method == 'POST':
        try:
            VALUE = request.form['rating']
            star = Rating(member_no=g.user.member_no,
                          book_no=book_no,
                          rating=int(VALUE))
            db.session.add(star)

            book = Storybook.query.get(book_no)

            if book.avg == 0:
                book.avg = VALUE

            else:
                book_avg =db.session.query(func.avg(Rating.rating))\
                    .join(Storybook)\
                    .filter(Rating.book_no == book.book_no)
                book.avg = book_avg
            db.session.commit()
            
            book = Storybook.query.get(book_no)
            
            if book.avg == 0:
                book.avg = VALUE
            else:
                book_avg = Rating.query.with_entities(Rating.book_no, func.avg(Rating.rating))\
                                 .filter(book.book_no == Rating.book_no)\
                                 .group_by(Rating.book_no).first()[1]
                book.avg = book_avg
            db.session.commit()
            
        except:
            error = "평점을 매겨주세요!"
    
        if error is None:
            return redirect(url_for('main.index'))
    
    else:
        isIt = Rating.query.filter(and_(Rating.member_no==g.user.member_no,
                                        Rating.book_no==book_no)).first()
          
    return render_template("/book/bookstar.html", error=error, book_no=book_no, book=book, isIt=isIt)


@bp.route('/readbook/<int:book_no>/')
def readbook(book_no):
    book = Storybook.query.get_or_404(book_no)
    image = Image.query.get(book_no)
    content = book.book_con
    DIVN = [220, 320, 420, 520, 620]
    storyArray = []
    
    filename=str(book.book_no)+'.mp3'
    audio = 'audio/'+filename
    if not book.speak_path:
        tts=gTTS(text=content, lang='ko')
        audio_path = '../project/BeAwriter/static/audio/'+filename
        tts.save(audio_path)
        
        book.speak_path = audio_path
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
    
    return render_template("/book/readbook.html", book=book, storyArray=storyArray, sa1=storyArray[1], sa2=storyArray[2], image=image,  book_no=book_no, audio=audio)
    


