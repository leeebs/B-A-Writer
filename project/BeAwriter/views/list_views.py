from email.policy import default
from flask import Blueprint, render_template, url_for, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from BeAwriter import db
from BeAwriter.models import *

bp = Blueprint('list', __name__, url_prefix='/list')

@bp.route('/booklist')
def booklist():
    page = request.args.get('page', type=int, default=1)
    book_list = Storybook.query.order_by(Storybook.book_date.desc())
    book_list=book_list.paginate(page, per_page=10)
    return render_template('main/booklist.html', book_list=book_list)