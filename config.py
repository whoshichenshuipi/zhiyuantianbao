import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 验证码类型 math 数字计算 char 字符验证
    CAPTCHA_TYPE = 'math'
    PROFILE = 'uploadPath'

    SECRET_KEY = os.environ.get('SECRET_KEY') or '@57NF6iA6jsvFpMZ'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 根据环境变量选择缓存类型，例如在开发环境可以用'simple'，生产环境可以用'redis'等
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300

    # 配置 Swagger
    SWAGGER = {
        'title': '后端接口 API',
        'version': '1.0.0',  # 使用 Swagger UI v3
        'description': '管理端接口api',
        'specs_route': '/swagger-ui/index.html',  # 自定义 Swagger UI 的路由
        'swagger_ui_bundle_js': '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js',
        'swagger_ui_standalone_preset_js': '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js',
        'jquery_js': '//unpkg.com/jquery@2.2.4/dist/jquery.min.js',
        'swagger_ui_css': '//unpkg.com/swagger-ui-dist@3/swagger-ui.css',
        'static_url_path': '/flasgger_static/',
        'swagger_ui': True
    }

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/zhiyuan?charset=utf8&auth_plugin=mysql_native_password'
    SQLALCHEMY_ECHO = False


class UatConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/zhiyuan?charset=utf8&auth_plugin=mysql_native_password'
    SQLALCHEMY_ECHO = False


class TestConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/zhiyuan?charset=utf8&auth_plugin=mysql_native_password'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/zhiyuan?charset=utf8&auth_plugin=mysql_native_password'


config = {
    'dev': DevConfig,
    'uat': UatConfig,
    'test': TestConfig,
    'prod': ProdConfig
}
