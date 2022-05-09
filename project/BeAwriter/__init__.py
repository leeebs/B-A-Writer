from flask import Flask, session
# from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import config

db = SQLAlchemy()
migrate = Migrate()
# sess = Session()
   
def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SECRET_KEY'] = 'SECRET KEYS'
    
    # 세션
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SECRET_KEY'] = 'super secret key'
    
    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    # 모델
    from . import models
    
        # 관리자 페이지    
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='B a writer', template_mode='bootstrap3')
    admin.add_view(ModelView(models.Member, db.session))
    admin.add_view(ModelView(models.Storybook, db.session))
    admin.add_view(ModelView(models.CoverImage, db.session))
    admin.add_view(ModelView(models.Pageimage, db.session))
    admin.add_view(ModelView(models.Question, db.session))
    admin.add_view(ModelView(models.QuestionComment, db.session))
    
    # 블루프린트
    from .views import main_views, auth_views, qna_views, book_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(book_views.bp)
    app.register_blueprint(qna_views.bp)

    # 필터
    from filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime



    return app