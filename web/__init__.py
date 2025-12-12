from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
import flask_excel as excel
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
from flasgger import Swagger
from flask_cors import CORS

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'

moment = Moment()

cache = Cache()

scheduler = BackgroundScheduler()


def create_app(config_name):
    app = Flask(__name__)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 配置CORS,允许前端跨域访问
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:80", "http://127.0.0.1:80"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    moment.init_app(app)

    db.init_app(app)

    login_manager.init_app(app)

    #使用init_app()初始化缓存
    cache.init_app(app)

    from .routes import main_routes as base_blueprint
    app.register_blueprint(base_blueprint)

    swagger = Swagger(app)

    excel.init_excel(app)
    return app

