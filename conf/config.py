import os


class BaseConfig:
    # ------------------------------
    # 服务器配置
    # ------------------------------
    DEBUG = True
    HOST_ADAPTER = os.getenv('HOST_ADAPTER', 'eth0')
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 8000
    USE_RELOADER = False
    CSRF_ENABLED = True
    CORS_RESOURCES = {r"/api/*": {"origins": "*"}}
    PROD_NAME = 'FlaskExample'
    SERVICE_NAME = 'FlaskExample'
    CURRENT_VERSION = os.getenv('CURRENT_VERSION', 'v0.0.1')
    SECRET_KEY = '\xbb2\xe1\x0cL\xbd\xb6\x9a\xf2iZ\xb6O\xed\x97\x97l3ZyN\x94N\xc3'



