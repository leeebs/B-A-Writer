from ast import Num
from audioop import ratecv
from flask import Blueprint, render_template, url_for, request, session, g
from regex import R
from sqlalchemy import Integer
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect, secure_filename

from BeAwriter import db
from BeAwriter.models import *
from datetime import datetime


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET', 'POST'])
def index():
    # total = db.session.query(Rating.rating,func.avg(Rating.rating)).group_by(Rating.book_no)

    page = request.args.get('page', type=int, default=1)
    book_list = Storybook.query.order_by(Storybook.book_date.desc())
    book_mem_name = []
    book_avg = []

    for book in book_list:
        member = Member.query.get(book.member_no)
        # rati = Rating.query.get(book.book_no)
        book_mem_name.append(member.member_name)
        # book_avg.append(db.session.query(func.avg(rati.rating)).group_by(rati.book_no).all())
        book_avg = Rating.query.with_entities(Rating.book_no, func.avg(Rating.rating))\
            .filter(book.book_no == Rating.book_no)\
            .group_by(Rating.book_no).all()[0]
    book_list = book_list.paginate(page, per_page=3)


    star_mem_name = []
    star_book_title=[]
    star_book_date=[]
    star_avg = []

    star_list = Rating.query.group_by(Rating.book_no)
    for star in star_list:
        member = Member.query.get(star.member_no)
        book = Storybook.query.get(star.book_no)
        star_mem_name.append(member.member_name)
        star_book_title.append(book.book_title)
        star_book_date.append(book.book_date)
        star_avg = star.query.with_entities(func.avg(Rating.rating))\
            .filter(book.book_no == star.book_no)\
            .group_by(Rating.book_no).all()[0]

    star_list = star_list.paginate(page, per_page=3)

    return render_template('main/main.html', book_list=book_list, page = page, book_mem_name = book_mem_name, book_rate=book_avg,
        star_list=star_list, star_mem_name=star_mem_name, star_book_title=star_book_title, star_book_date=star_book_date, star_rate=star_avg)
    # return render_template('main/main.html', star_list=star_list, star_mem_name=star_mem_name, star_book_title=star_book_title, star_book_date=star_book_date, star_rate=star_avg)

# 기본 화면 _ 오래된 순으로 표시
@bp.route('/datelist')
def datelist():
    page = request.args.get('page', type=int, default=1)
    book_list = Storybook.query.order_by(Storybook.book_date.asc())
    book_mem_name = []
    book_avg=[]
    for book in book_list:
        member = Member.query.get(book.member_no)
        rati = Rating.query.get(book.member_no)
        book_mem_name.append(member.member_name)
        book_avg.append(db.session.query(rati.book_no, func.avg(rati.rating)).group_by(rati.book_no))
    book_list = book_list.paginate(page, per_page=9)
    return render_template('main/datelist.html', book_list=book_list, page=page, book_mem_name=book_mem_name, rate=book_avg)

# 별점
@bp.route('/starlist')
def starlist():
    page = request.args.get('page', type=int, default=1)
    star_list = Rating.query.order_by(Rating.book_no.desc()).where(Rating.member_no == g.user.member_no)
    star_mem_name = []
    star_book_title = []
    star_book_date = []
    book_avg = []
    for star in star_list:
        member = Member.query.get(star.member_no)
        book = Storybook.query.get(star.book_no)
        star_mem_name.append(member.member_name)
        star_book_title.append(book.book_title)
        star_book_date.append(book.book_date)
        book_avg.append(db.session.query(star.book_no, func.avg(star.rating)).group_by(star.book_no))

    star_list = star_list.paginate(page, per_page=9)

    return render_template('main/starlist.html', star_list=star_list, star_mem_name=star_mem_name, star_book_title=star_book_title,
        star_book_date=star_book_date, rate=book_avg)

# 내가 만든
@bp.route('/mylist', methods=['GET', 'POST'])
def mylist():
    page = request.args.get('page', type=int, default=1)
    book_mem_name = []
    my_list = Storybook.query.group_by(Storybook.member_no).where(Storybook.member_no == g.user.member_no).order_by(Storybook.book_no.asc())
    for me in my_list:
        member = Member.query.get(me.member_no)
        book_mem_name.append(member.member_name)
    my_list = my_list.paginate(page, per_page=9)

    if my_list:
        total = Rating.query.with_entities(func.avg(Rating.rating))\
        .group_by(Rating.book_no).first()[0]

    return render_template('main/mylist.html', my_list=my_list, page=page, book_mem_name=book_mem_name, rate=total)