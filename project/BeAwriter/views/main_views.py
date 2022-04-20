from flask import Blueprint, render_template, url_for, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect, secure_filename

from BeAwriter import db
from BeAwriter.models import *
from datetime import datetime


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    kw1 = request.args.get('kw', type=str, default='')
    book_list = Storybook.query.order_by(Storybook.book_date.desc())
    if kw1:
        search = '%%{}%%'.format(kw1)
        sub_query = db.session.query(Storybook.book_no, Storybook.book_no, Storybook.book_title, Member.member_name)\
            .join(Member, Storybook.member_no == Member.member_no).subquery()
        book_list = book_list.join(Member)\
            .outerjoin(sub_query, sub_query.c.member_no == Storybook.member_no)\
            .filter(Storybook.book_no.ilike(search) |
                    Storybook.book_title.ilike(search) |
                    Member.member_name.ilike(search)|
                    Storybook.book_date.ilike(search)).distinct()

    kw2 = request.args.get('kw', type=str, default='')
    star_list = Storybook.query.order_by(Rating.rating.desc())
    if kw1:
        search = '%%{}%%'.format(kw2)
        sub_query = db.session.query(Storybook.book_no, Storybook.book_title, Member.member_name)\
            .join(Rating, Member, Storybook.member_no == Rating.member_no, Storybook.member_no == Member.member_no).subquery()
        star_list = star_list.join(Member)\
            .outerjoin(sub_query, sub_query.c.member_no == Storybook.member_no)\
            .filter(Storybook.book_no.ilike(search) |
                    Storybook.book_title.ilike(search) |
                    Member.member_name.ilike(search) |
                    Rating.rating.ilike(search)).distinct()

    return render_template('main/main.html', book_list=book_list, star_list = star_list, kw1=kw1, kw2=kw2)

@bp.route('/booklist')
def booklist():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    book_list = Storybook.query.order_by(Storybook.book_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Storybook.book_no, Storybook.book_title, Member.member_name)\
            .join(Member, Storybook.member_no == Member.member_no).subquery()
        book_list = book_list.join(Member)\
            .outerjoin(sub_query, sub_query.c.member_no == Storybook.member_no)\
            .filter(Storybook.book_no.ilike(search) |
                    Storybook.book_title.ilike(search) |
                    Member.member_name.ilike(search)).distinct()
    book_list = book_list.paginate(page, per_page=10)
    return render_template('main/booklist.html', book_list=book_list, page=page, kw=kw)

# 최신
# @bp.route('/datelist')
# def datelist():
#     page = request.args.get('page', type=int, default=1)
#     book_list = Storybook.query.order_by(Storybook.create_date.desc())
#     book_list = book_list.paginate(page, per_page=10)
#     return render_template('main/booklist.html', book_list=book_list, page=page)

# 별점
# @bp.route('/starlist')
# def starlist():
#     page = request.args.get('page', type=int, default=1)
#     book_list = Rating.query.order_by(Rating.rating.desc())
#     book_list = book_list.paginate(page,per_page=10)
#     return render_template('main/booklist.html', book_list-book_list, page=page)

# 내가 만든
# @bp.route('/mylist')
# def mylist():
#     page = request.args.get('page', type=int, default=1)
#     book_list = Rating.query.order_by(Rating.rating.desc())
#     book_list = book_list.paginate(page,per_page=10)
#     return render_template('main/booklist.html', book_list-book_list, page=page)