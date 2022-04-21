from ast import Num
from flask import Blueprint, render_template, url_for, request, session, g
from sqlalchemy import Integer
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
    book_mem_name = []
    for book in book_list:
        member = Member.query.get(book.member_no)
        # rating = Rating.query.get(book.book_no)
        book_mem_name.append(member.member_name)

    book_list = book_list.paginate(page, per_page=3)


    star_list = Rating.query.order_by(Rating.rating.desc())
    star_mem_name = []
    book_title = []
    book_date = []
    for book in star_list:
        member = Member.query.get(book.member_no)
        book = Storybook.query.get(Storybook.member_no)
        star_mem_name.append(member.member_name)
        book_title.append(book.book_title)
        book_date.append(book.book_date)

    star_list = star_list.paginate(page, per_page=3)

    return render_template('main/main.html', book_list=book_list, page = page, book_mem_name = book_mem_name, book_title=book_title, book_date = book_date, star_mem_name = star_mem_name)

# 기본 화면 _ 오래된 순으로 표시
@bp.route('/datelist')
def datelist():
    page = request.args.get('page', type=int, default=1)
    book_list = Storybook.query.order_by(Storybook.book_date.asc())
    book_mem_name = []
    for book in book_list:
        member = Member.query.get(book.member_no)
        book_mem_name.append(member.member_name)
    book_list = book_list.paginate(page, per_page=10)
    return render_template('main/datelist.html', book_list=book_list, page=page, book_mem_name=book_mem_name)

# 별점
@bp.route('/starlist')
def starlist():
    page = request.args.get('page', type=int, default=1)
    star_list = Rating.query.order_by(Rating.rating.desc())
    book_mem_name = []
    book_title = []
    book_date = []
    book_no
    for book in star_list:
        member = Member.query.get(book.member_no)
        book = Storybook.query.get(book.member_no)
        book_mem_name.append(member.member_name)
        book_title.append(book.book_title)
        book_date.append(book.book_date)
        book_no = book.book_no

    star_list = star_list.paginate(page, per_page=10)
    return render_template('main/starlist.html', star_list=star_list, page=page, book_mem_name=book_mem_name, book_title=book_title, book_date=book_date, book_no=book_no)

# 내가 만든
@bp.route('/mylist', methods=['GET', 'POST'])
def mylist():
    page = request.args.get('page', type=int, default=1)
    book_mem_name = []
    my_list = Storybook.query.group_by(Storybook.member_no).where(Storybook.member_no == g.user.member_no)
    for me in my_list:
        member = Member.query.get(me.member_no)
        book_mem_name.append(member.member_name)
    my_list = my_list.paginate(page, per_page=10)
    return render_template('main/mylist.html', my_list=my_list, page=page, book_mem_name=book_mem_name)