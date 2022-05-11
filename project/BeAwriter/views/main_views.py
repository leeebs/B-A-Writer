from flask import Blueprint, render_template, request, g

from BeAwriter.models import Storybook, Member, CoverImage, Rating


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', type=int, default=1)
    book_list = Storybook.query.order_by(Storybook.book_no.desc())
    book_mem_name = []
    book_img_path = []
    book_avg = []
    for book in book_list:
        member = Member.query.get(book.member_no)
        book_mem_name.append(member.member_name)
        image = CoverImage.query.get(book.book_no)
        if image:
            book_img_path.append(image.maked_img_path)
        else:
            book_img_path.append(None)
        book_avg.append(book.avg)
            
    book_list = book_list.paginate(page, per_page=3)
    
    star_mem_name = []
    star_img_path = []
    star_avg=[]

    star_list = Storybook.query.order_by(Storybook.avg.desc())
    for star in star_list:
        member = Member.query.get(star.member_no)
        star_mem_name.append(member.member_name)
        image = CoverImage.query.get(star.book_no)
        if image:
            star_img_path.append(image.maked_img_path)
        else:
            star_img_path.append(None)
        star_avg.append(star.avg)

    star_list = star_list.paginate(page, per_page=3)

    return render_template('main/main.html', book_list=book_list, page = page, book_mem_name = book_mem_name, book_avg=book_avg,book_img_path=book_img_path,
        star_list=star_list, star_mem_name=star_mem_name, star_avg=star_avg, star_img_path=star_img_path)
    
# 기본 화면 _ 오래된 순으로 표시
@bp.route('/datelist')
def datelist():
    page = request.args.get('page', type=int, default=1)
    book_list = Storybook.query.order_by(Storybook.book_date.asc())
    book_mem_name = []
    book_avg = []
    book_img_path = []

    for book in book_list:
        member = Member.query.get(book.member_no)
        book_mem_name.append(member.member_name)
        book_avg.append(book.avg)
        image = CoverImage.query.get(book.book_no)
        if image:
            book_img_path.append(image.maked_img_path)
        else:
            book_img_path.append(None)
    book_list = book_list.paginate(page, per_page=9)
    return render_template('main/datelist.html', book_list=book_list, page=page, book_mem_name=book_mem_name, book_rate=book_avg, book_img_path=book_img_path)

# 별점
@bp.route('/starlist')
def starlist():
    page = request.args.get('page', type=int, default=1)
    star_list = Storybook.query.order_by(Storybook.avg.desc())
    star_mem_name = []
    star_rate = []
    star_book_title = []
    star_book_date = []
    book_avg = []
    book_img_path=[]

    for star in star_list:
        member = Member.query.get(star.member_no)
        star_mem_name.append(member.member_name)
        star_book_title.append(star.book_title)
        star_book_date.append(star.book_date)
        book_avg.append(star.avg)
        star_rate.append(star.avg)
        image = CoverImage.query.get(star.book_no)
        if image:
            book_img_path.append(image.maked_img_path)
        else:
            book_img_path.append(None)

    star_list = star_list.paginate(page, per_page=12)

    return render_template('main/starlist.html', star_list=star_list, star_mem_name=star_mem_name, star_rate=star_rate, book_img_path=book_img_path)

# 내가 만든
@bp.route('/mylist', methods=['GET', 'POST'])
def mylist():
    page = request.args.get('page', type=int, default=1)
    book_mem_name = []
    my_list = Storybook.query.filter(Storybook.member_no == g.user.member_no).order_by(Storybook.book_no.asc())
    book_rate = []
    book_img_path = []
    for me in my_list:
        member = Member.query.get(me.member_no)
        book_mem_name.append(member.member_name)
        book_rate.append(me.avg)
        image = CoverImage.query.get(me.book_no)
        if image:
            book_img_path.append(image.maked_img_path)
        else:
            book_img_path.append(None)
    my_list = my_list.paginate(page, per_page=12)

    return render_template('main/mylist.html', my_list=my_list, page=page, book_mem_name=book_mem_name, book_rate=book_rate, book_img_path=book_img_path)


# 내가 별점 준 전체
@bp.route('/mystarlist', methods=['GET', 'POST'])
def mystarlist():
    page = request.args.get('page', type=int, default=1)
    star_mem_name = []
    star_book_title=[]
    star_book_date=[]
    star_rate=[]
    book_img_path = []
    star_list = Rating.query.filter(Rating.member_no == g.user.member_no).order_by(Rating.book_no.asc())
    for star in star_list:
        member = Member.query.get(star.member_no)
        book = Storybook.query.get(star.book_no)
        star_mem_name.append(member.member_name)
        star_book_title.append(book.book_title)
        star_book_date.append(book.book_date)
        star_rate.append(book.avg)
        image = CoverImage.query.get(star.book_no)
        if image:
            book_img_path.append(image.maked_img_path)
        else:
            book_img_path.append(None)

    star_list = star_list.paginate(page, per_page=12)
    return render_template('main/mystarlist.html', star_list=star_list, page=page, star_mem_name=star_mem_name, star_book_title=star_book_title,
        star_book_date=star_book_date, star_rate=star_rate, book_img_path=book_img_path)