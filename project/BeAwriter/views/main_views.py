from flask import Blueprint, render_template
from BeAwriter.models import *

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return 'main'
    
@bp.route('/login')
def login():
    return render_template('member/login.html')