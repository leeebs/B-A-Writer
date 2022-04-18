from flask import Blueprint, render_template, url_for, request, g
from werkzeug.utils import redirect, secure_filename

from BeAwriter import db
from BeAwriter.models import *

bp = Blueprint('book', __name__, url_prefix='/book')

@bp.route('/', methods=('GET','POST'))
def make():
    msg = None
    
    if request.method == 'POST':
        content = request.form['content']
        if not content:
            msg = "키워드나 짧은 문장을 작성해주세요!"
        else:
            # 디비 추가..
            sb = Storybook(book_con=content,
                           member_no=g.user.member_no)
            db.session.add(sb)
            db.session.commit()
            
        if msg is None:
            return redirect(url_for('book.make')) #동화생성페이지로 수정
        
    return render_template('book/makebook.html', msg=msg)


@bp.route('/cover', methods=('GET','POST'))
def cover():
    msg = None
    
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            msg = "파일을 넣고 제출 버튼을 눌러주세요."
        else:
            file_name = secure_filename(f.filename)
            f.save(file_name)
            # img = Image()
            
        if msg is None:
            return redirect(url_for('main.index')) #동화생성페이지로 수정
            
    return render_template('book/bookcover.html', msg=msg)