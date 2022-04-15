from flask import Blueprint, render_template, request
from BeAwriter.models import *
from forms import QuestionForm, QuestionCommentForm
from datetime import datetime

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/main')
def index():
    return render_template('main/main.html')
    
@bp.route('/login')
def login():
    return render_template('member/login.html')

@bp.route('/register')
def register():
    return render_template('member/register.html')

@bp.route('/readbook')
def readbook():
    return render_template('book/readbook.html')

@bp.route('/makebook')
def makebook():
    return render_template('book/makebook.html')

@bp.route('/booklist')
def booklist():
    return render_template('main/booklist.html')

@bp.route('/bookstar')
def bookstar():
    return render_template('book/bookstar.html')

@bp.route('/qnalist')
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
 
@bp.route('/qnawrite')
def QnA_write():
    return render_template('qna/FAQ_write.html')

@bp.route('/qna/<int:question_no>/')
def QnA(question_no):
    form = QuestionCommentForm()
    question = Question.query.get_or_404(question_no)
    return render_template('qna/FAQ.html', question=question, form=form)

