from flask import Blueprint, render_template, url_for, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect, secure_filename

from BeAwriter import db
from BeAwriter.models import *

bp = Blueprint('qna', __name__, url_prefix='/qna')

@bp.route('/qnawrite',  methods=('GET','POST'))
def qnawrite():
    error = None
    
    if request.method == 'POST':

        TITLE = request.form['title']
        CONTENT = request.form['content']
        if not TITLE:
            error = "문의 제목을 입력해주세요."
        elif not CONTENT:
            error = "문의 하실 내용을 입력해주세요."
        else:
            question = Question(ques_title=TITLE,
                                ques_con=CONTENT,
                                member_no=g.user.member_no)
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('qna.qnalist'))

    return render_template("/qna/FAQ_write.html", error=error)
    
@bp.route('/qnalist')
def qnalist():
    return render_template("/qna/FAQ_list.html")
