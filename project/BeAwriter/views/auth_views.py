from flask import Blueprint, render_template, url_for, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from BeAwriter import db
from BeAwriter.models import Member

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET','POST'))
def login():
    error = None
    
    if request.method == 'POST':
        ID = request.form['id']
        PW = request.form['pw']
        if not ID:
            error = "아이디를 입력해주세요."
        elif not PW:
            error = "비밀번호를 입력해주세요."
        else:
            user = Member.query.filter_by(member_id=ID).first()
            if not user:
                error = "존재하지 않는 아이디 입니다."
            elif not check_password_hash(user.member_password, PW):
                error = "비밀번호를 확인해주세요."
            
        if error is None:
            session.clear()
            session['user_no'] = user.member_no
            return redirect(url_for('main.index'))
    
    return render_template('member/login.html',error=error)



@bp.route('/register/', methods=('GET', 'POST'))
def register():
    error = None
    if request.method == 'GET':
        return render_template("member/register.html")
    else:
        id = request.form['id']
        email = request.form['email']
        password = request.form['pw']
        re_password = request.form['re-password']
        name = request.form['name']

        val_id = Member.query.filter_by(member_id=id).first()
        val_email = Member.query.filter_by(member_email=email).first()

        if not(id and email and password and re_password and name):
            error = "모든 정보를 입력해 주세요"
        elif password != re_password:
            error = "비밀번호가 일치하지 않습니다"
        elif val_id:
            error = "이미 사용 중인 아이디입니다"
        elif val_email:
            error = "이미 사용 중인 이메일입니다"

        elif error is None:
            m = Member()
            m.member_id = id
            m.member_email = email
            m.member_password = generate_password_hash(password)
            m.member_name = name

            db.session.add(m)
            db.session.commit()
            return redirect(url_for('main.index'))

    return render_template("member/register.html", error=error)

@bp.before_app_request
def load_logged_in_user():
    user_no = session.get('user_no')
    if user_no is None:
        g.user = None
    else:
        g.user = Member.query.get(user_no)
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))