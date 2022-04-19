from email.policy import default
from flask import Blueprint, render_template, url_for, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from BeAwriter import db
from BeAwriter.models import *


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('main/main.html')
