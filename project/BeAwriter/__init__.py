from flask import Flask, session
# from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()
# sess = Session()
   
def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    # 세션
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SECRET_KEY'] = 'super secret key'
    # sess.init_app(app)
    
    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    # 모델
    from . import models
    
    # 블루프린트
    from .views import main_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)

    
    return app