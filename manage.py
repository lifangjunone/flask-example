from flask import Flask
from conf import config
from flask_cors import CORS
from flask_script import Manager, Server
from apis import API_VERSION_MAPPING, VERSIONS_ALLOWED


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


app = create_app()
manager = Manager(app)

manager.add_command('runserver', Server(host=app.config['SERVER_HOST'],
                                        port=app.config['SERVER_PORT'],
                                        use_debugger=app.config['DEBUG'], use_reloader=app.config['USE_RELOADER']))

if __name__ == '__main__':
    manager.run()
