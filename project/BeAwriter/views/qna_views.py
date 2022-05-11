from flask import Blueprint, render_template, url_for, request, g
from werkzeug.utils import redirect
from BeAwriter.forms import QuestionForm, AnswerForm

from BeAwriter import db
from BeAwriter.models import Question, QuestionComment, Member

import datetime
from pytz import timezone, utc

bp = Blueprint('qna', __name__, url_prefix='/qna')

KST = timezone('Asia/Seoul')
now = datetime.datetime.utcnow()

@bp.route('/qnawrite/', methods=('GET', 'POST'))
def qnawrite():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data,
                                content=form.content.data,
                                member_no=g.user.member_no,
                                ques_date = utc.localize(now).astimezone(KST))
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('qna.qnalist'))
    return render_template("/qna/FAQ_write.html", form=form)


@bp.route('/qnalist')
def qnalist():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    question_list = Question.query.order_by(Question.ques_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(QuestionComment.question_no, QuestionComment.comment_con, Member.member_id, Member.member_name) \
            .join(Member, QuestionComment.member_no == Member.member_no).subquery()
        question_list = question_list \
            .join(Member) \
            .outerjoin(sub_query, sub_query.c.question_no == Question.question_no) \
            .filter(Question.subject.ilike(search) |  # 질문 제목
                    Question.content.ilike(search) |  # 질문 내용
                    Member.member_name.ilike(search) |  # 질문 작성자
                    sub_query.c.comment_con.ilike(search)   # 답변 내용
                    ) \
            .distinct()
    question_list = question_list.paginate(page, per_page=10)
    return render_template('qna/FAQ_list.html', question_list=question_list, page=page, kw=kw)

@bp.route('/<int:question_no>/')
def QnA(question_no):
    form = AnswerForm()
    question = Question.query.get_or_404(question_no)
    return render_template('qna/FAQ.html', question=question, form=form)

@bp.route('/answerwrite/<int:question_no>', methods=('POST',))
def answerwrite(question_no):
    form = AnswerForm()
    question = Question.query.get_or_404(question_no)
    content = request.form['content']
    if form.validate_on_submit():
        answer = QuestionComment(content=content, comment_date=utc.localize(now).astimezone(KST), member_no=g.user.member_no)
        question.questioncomment_set.append(answer)
        db.session.commit()
        return redirect(url_for('qna.QnA', question_no= question_no))
    return render_template('qna/FAQ.html', question=question, form=form)


@bp.route('/modify/<int:question_no>', methods=('GET', 'POST'))
def modify(question_no):
    question = Question.query.get_or_404(question_no)
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            db.session.commit()
            return redirect(url_for('qna.QnA', question_no=question_no))
    else:  # GET 요청
        form = QuestionForm(obj=question)
    return render_template("/qna/FAQ_write.html", form=form)


@bp.route('/answerdelete/<int:question_comment_no>')
def answerdelete(question_comment_no):
    answer = QuestionComment.query.get_or_404(question_comment_no)
    question_no = answer.question.question_no
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for('qna.QnA', question_no=question_no))

@bp.route('/questiondelete/<int:question_no>')
# @login_required
def questiondelete(question_no):
    question = Question.query.get_or_404(question_no)
    # if g.user != question.member_no:
    #     flash('삭제권한이 없습니다')
    #     return redirect(url_for('qna.QnA', question_no=question_no))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('qna.qnalist'))