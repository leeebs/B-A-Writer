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
    book_mem_name = []
    for book in book_list:
        member = Member.query.get(book.member_no)
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

# 기본 화면
@bp.route('/booklist')
def booklist():
    page = request.args.get('page', type=int, default=1)
    book_list = Storybook.query.order_by(Storybook.book_date.asc())
    book_mem_name = []
    for book in book_list:
        member = Member.query.get(book.member_no)
        book_mem_name.append(member.member_name)
    book_list = book_list.paginate(page, per_page=10)
    return render_template('main/booklist.html', book_list=book_list, page=page, book_mem_name=book_mem_name)

# 별점
@bp.route('/starlist')
def starlist():
    page = request.args.get('page', type=int, default=1)
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

    star_list = star_list.paginate(page, per_page=10)
    return render_template('main/booklist.html', star_list=star_list, page=page)

# 내가 만든
# @bp.route('/mylist')
# def mylist():
#     page = request.args.get('page', type=int, default=1)
#     book_list = Rating.query.order_by(Rating.rating.desc())
#     book_list = book_list.paginate(page,per_page=10)
#     return render_template('main/booklist.html', book_list-book_list, page=page)