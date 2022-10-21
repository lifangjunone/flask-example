from flask import Flask
from conf import config
from flask_cors import CORS
from flask_script import Manager, Server
from flask_jwt_extended import jwt_required
from flask import request, jsonify
from apis import API_VERSION_MAPPING, VERSIONS_ALLOWED
from common.return_data import TokenInvalid, get_return_data

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


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.BaseConfig)
    _register_extensions(app)
    _registry_blueprint(app)
    return app


@jwt_required()
def _verify_token():
    pass


app = create_app()


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
    # print("----after_request----")
    resp = response.json
    # 必须返回response参数
    msg = resp.get('msg', None) if resp else None
    if msg in TOKEN_ERROR_INFO:
        return jsonify(get_return_data(TokenInvalid, {}, msg))
    return response


manager = Manager(app)
manager.add_command('runserver', Server(host=app.config['SERVER_HOST'],
                                        port=app.config['SERVER_PORT'],
                                        use_debugger=app.config['DEBUG'], use_reloader=app.config['USE_RELOADER']))

if __name__ == '__main__':
    manager.run()
