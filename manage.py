from flask import Flask
from flask_cors import CORS
from flask_script import Manager, Server, Shell
from flask_jwt_extended import jwt_required
from flask import request, jsonify
from apis import API_VERSION_MAPPING, VERSIONS_ALLOWED
from common.return_data import TokenInvalid, get_return_data
from conf import celeryconfig
from common.extensions import celery, db, main_app_create_engine
from flask_jwt_extended import JWTManager
from middleware.global_middleware import RequestFilter
from conf.config import BaseConfig
from common.log_handler import LogHandler
from conf.config import config_mapping
import os

TOKEN_ERROR_INFO = ['Signature verification failed', 'Invalid crypto padding', 'Token has expired']


def _get_url_prefix(blueprint):
    return "/api/{0}".format(str(blueprint))


def _register_extensions(app):
    """注册扩展模块

    :param app:
    :return:
    """
    cors = CORS()
    cors.init_app(app, resources=app.config['CORS_RESOURCES'], supports_credentials=True)


def _registry_blueprint(app):
    for blueprint in VERSIONS_ALLOWED:
        app.register_blueprint(blueprint=API_VERSION_MAPPING[blueprint], url_prefix=_get_url_prefix(blueprint))


def init_celery(app, celery):
    """
    :param app:
    :param celery:
    :return:
    """
    celery.config_from_object(celeryconfig)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_test_data():
    """
    insert test data
    :return:
    """
    with main_app_create_engine.connect() as con:
        con.execute('INSERT INTO user (username, age, sex,  is_delete)VALUES ("libai", 20, "man", 0)')


def create_app(env_name):
    """应用工厂方法
    :param env_name  environment name
    :return: flask_app
    """
    app = Flask(__name__)
    app.config.from_object(config_mapping[env_name])
    _register_extensions(app)
    _registry_blueprint(app)
    init_celery(app, celery)

    # Init SQLAlchemy
    if BaseConfig.ENV == 'testing':
        with app.app_context():
            db.init_app(app)
            db.create_all()
            create_test_data()

    # NO DEBUG MODE RUN
    if not app.debug:
        LogHandler(app)
    return app


@jwt_required()
def _verify_token():
    pass


app = create_app(os.getenv('ENVIRONMENT', 'testing'))


@app.before_request
def before_request():
    """
    这个钩子会在每次客户端访问视图的时候执行
    # 可以在请求之前进行用户的身份识别，以及对于本次访问的用户权限等进行判断。..
    """
    # print("----before_request----")
    # Session.expire()
    # db.session.expire_all()
    from urllib.parse import urlparse
    path_list = urlparse(request.base_url).path.split('/')
    if 'example_api' in request.base_url or 'example_api' in path_list:
        pass
    else:
        _verify_token()


@app.after_request
def after_request(response):
    resp = response.json
    msg = resp.get('msg', None) if resp else None
    if msg in TOKEN_ERROR_INFO:
        return jsonify(get_return_data(TokenInvalid, {}, msg))
    return response


def make_shell_context():
    return dict(app=app)


# use Manage management app
manager = Manager(app)

# 命令行工具
manager.add_command('shell', Shell(make_context=make_shell_context))
# use JWTManager management JWT
jwt = JWTManager(app)
# Init middleware
app.wsgi_app = RequestFilter(app.wsgi_app)
manager.add_command('runserver', Server(host=app.config['SERVER_HOST'],
                                        port=app.config['SERVER_PORT'],
                                        use_debugger=app.config['DEBUG'], use_reloader=app.config['USE_RELOADER']))

if __name__ == '__main__':
    manager.run()
