from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect
from BeAwriter.models import *

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return 'main!'