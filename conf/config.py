

class BaseConfig:

    CORS_RESOURCES = {r"/api/*": {"origins": "*"}}
    DEBUG = True
    SERVER_PORT = 9000
    SERVER_HOST = "0.0.0.0"


