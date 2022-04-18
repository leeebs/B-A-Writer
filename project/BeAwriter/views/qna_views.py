from flask import Blueprint, render_template, url_for, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect, secure_filename

from BeAwriter import db
from BeAwriter.models import *
from datetime import datetime

bp = Blueprint('qna', __name__, url_prefix='/qna')

@bp.route('/qnawrite',  methods=('GET','POST'))
def qnawrite():
    error = None
    if request.method == 'POST':

        TITLE = request.form['title']
        CONTENT = request.form['content']
        if not TITLE:
            error = "문의제목을 입력해주세요."
        elif not CONTENT:
            error = "문의내용을 입력해주세요."
        else:
            question = Question(question_no=4,
                                    ques_title=TITLE,
                                    ques_con=CONTENT,
                                    
                                    member_no = 4)
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('qna.qnalist'))

    return render_template("/qna/FAQ_write.html", error=error)



@bp.route('/list/')
def QnA_list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    question_list = Question.query.order_by(Question.ques_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(QuestionComment.question_no, QuestionComment.comment_con, Member.member_id) \
            .join(Member, QuestionComment.member_no == Member.member_no).subquery()
        question_list = question_list \
            .join(Member) \
            .outerjoin(sub_query, sub_query.c.question_no == Question.question_no) \
            .filter(Question.ques_title.ilike(search) |  # 질문 제목
                    Question.ques_con.ilike(search) |  # 질문 내용
                    Member.member_id.ilike(search) |  # 질문 작성자
                    sub_query.c.comment_con.ilike(search)   # 답변 내용
             ) \
            .distinct()
    question_list = question_list.paginate(page, per_page=10)
    return render_template('qna/FAQ_list.html', question_list=question_list, page=page, kw=kw)

@bp.route('/<int:question_no>/')
def QnA(question_no):
    question = Question.query.get_or_404(question_no)
    return render_template('qna/FAQ.html', question=question)
