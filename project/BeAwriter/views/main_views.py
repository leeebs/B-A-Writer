from flask import Blueprint, render_template, url_for, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect, secure_filename

from BeAwriter import db
from BeAwriter.models import *
from datetime import datetime


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    page = request.args.get('page', type=int, default=1)
    book_list = Storybook.query.order_by(Storybook.book_date.desc())
    # book_list = 

    star_list = Rating.query.order_by(Rating.rating.desc())
    sub_query = db.session.query(Rating.book_no, Storybook.book_title, Member.member_name, Rating.rating, Member.member_no)\
            .join(Rating, Member, Storybook.book_no == Rating.book_no, Storybook.member_no == Member.member_no).subquery()
    star_list = star_list.join(Member, Storybook)\
        .outerjoin(sub_query, sub_query.c.book_no == Storybook.book_no, sub_query.c.member_no == Member.member_no)\
        .filter(Storybook.book_no |
                Storybook.book_title |
                Member.member_name |
                Rating.rating).distinct()
    star_list = star_list.paginate(page, per_page=3)

    return render_template('main/main.html', book_list=book_list, page = page)

@bp.route('/booklist')
def booklist():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    book_list = Storybook.query.order_by(Storybook.book_no)
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Storybook.book_no, Storybook.book_title, Member.member_name, Storybook.book_date)\
            .join(Member, Storybook.member_no == Member.member_no).subquery()
        book_list = book_list.join(Member)\
            .outerjoin(sub_query, sub_query.c.member_no == Storybook.member_no)\
            .filter(Storybook.book_no.ilike(search) |
                    Storybook.book_title.ilike(search) |
                    Member.member_name.ilike(search)|
                    Storybook.book_date.ilike(search)).distinct()
    book_list = book_list.paginate(page, per_page=10)
    return render_template('main/booklist.html', book_list=book_list, page=page, kw=kw)

# 오래된순
@bp.route('/datelist')
def datelist():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    book_list = Storybook.query.order_by(Storybook.book_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Storybook.book_no, Storybook.book_title, Member.member_name, Storybook.book_date)\
            .join(Member, Storybook.member_no == Member.member_no).subquery()
        book_list = book_list.join(Member)\
            .outerjoin(sub_query, sub_query.c.member_no == Storybook.member_no)\
            .filter(Storybook.book_no.ilike(search) |
                    Storybook.book_title.ilike(search) |
                    Member.member_name.ilike(search)|
                    Storybook.book_date.ilike(search)).distinct()
    book_list = book_list.paginate(page, per_page=10)
    return render_template('main/booklist.html', book_list=book_list, page=page, kw=kw)

# 별점
@bp.route('/starlist')
def starlist():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    star_list = Rating.query.order_by(Rating.rating.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Rating.book_no, Storybook.book_title, Member.member_name, Rating.rating)\
            .join(Rating, Member, Storybook.book_no == Rating.book_no, Storybook.member_no == Member.member_no).subquery()
        star_list = star_list.join(Member, Storybook)\
            .outerjoin(sub_query, sub_query.c.book_no == Storybook.book_no, sub_query.c.member_no == Member.member_no)\
            .filter(Storybook.book_no.ilike(search) |
                    Storybook.book_title.ilike(search) |
                    Member.member_name.ilike(search) |
                    Rating.rating.ilike(search)).distinct()
    star_list = star_list.paginate(page, per_page=10)
    return render_template('main/booklist.html', star_list=star_list, page=page, kw=kw)

# 내가 만든
# @bp.route('/mylist')
# def mylist():
#     page = request.args.get('page', type=int, default=1)
#     book_list = Rating.query.order_by(Rating.rating.desc())
#     book_list = book_list.paginate(page,per_page=10)
#     return render_template('main/booklist.html', book_list-book_list, page=page)