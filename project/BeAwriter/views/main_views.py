from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect
from BeAwriter.models import *


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/main')
def index():
    return render_template('main/main.html')
    
@bp.route('/login')
def login():
    return render_template('member/login.html')


