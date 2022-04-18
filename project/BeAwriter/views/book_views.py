from flask import Blueprint, render_template, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect, secure_filename

from BeAwriter import db
from BeAwriter.models import *

bp = Blueprint('book', __name__, url_prefix='/book')

@bp.route('/cover', methods=('GET','POST'))
def cover():
    msg = None
    
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            msg = "파일을 넣고 제출 버튼을 눌러주세요."
        else:
            f.save(secure_filename(f.filename))
            
        if msg is None:
            return redirect(url_for('main.index')) #동화생성페이지로 수정
            
    return render_template('book/bookcover.html', msg=msg)


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


