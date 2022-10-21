import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    # ------------------------------
    # 服务器配置
    # ------------------------------
    ENV = os.getenv("ENVIRONMENT", "testing")
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

    # ------------------------------
    # Mysql配置
    # ------------------------------
    MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT = os.getenv("MYSQL_PORT", 3306)
    MYSQL_USER = os.getenv("MYSQL_USER", 'root')
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", '123456')
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", 'test')
    MYSQL_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT,
                                                        MYSQL_DATABASE)

    # ------------------------------
    # Redis配置
    # ------------------------------
    REDIS_HOST = os.getenv("REDIS_HOST", '10.31.0.184')
    REDIS_PORT = os.getenv("REDIS_PORT", 8010)
    REDIS_DB = os.getenv("REDIS_DB", 5)
    REDIS_DB_CELERY_RESULT = os.getenv("REDIS_DB", 9)
    # REDIS_USER = os.getenv("REDIS_USER", "root")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "320qOnDMoKSBTYV7")

    # ------------------------------
    # Celery配置
    # ------------------------------
    if REDIS_PASSWORD:
        BROKER_URL = 'redis://:' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + str(REDIS_PORT) + '/' + str(REDIS_DB)
        RESULT_BACKEND = 'redis://:' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + str(REDIS_PORT) + '/' + \
                         str(REDIS_DB_CELERY_RESULT)
    else:
        BROKER_URL = 'redis://' + REDIS_HOST + ':' + str(REDIS_PORT) + '/' + str(REDIS_DB)
        RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + str(REDIS_PORT) + '/' + str(REDIS_DB_CELERY_RESULT)

    # ------------------------------
    # 日志配置 默认值：INFO
    # ------------------------------
    """
        CRITICAL = 50
        ERROR = 40
        WARNING = 30
        INFO = 20
        DEBUG = 10
        NOTSET = 0
    """
    GLOBAL_LOGLEVEL = 20

    # 日志文件存储路径
    LOG_DIR_PREFIX = _basedir + '/../logs/'
    # 日志文件命名
    LOG_FILE = LOG_DIR_PREFIX + SERVICE_NAME + '.log'


class ProductionConfig(BaseConfig):
    DEBUG = False
    # ------------------------------
    # 数据库连接配置
    # ------------------------------
    SQLALCHEMY_DATABASE_URI = BaseConfig.MYSQL_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_PROCESS_COUNT = os.getenv("MAX_PROCESS_COUNT", 4)


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    USE_RELOADER = True
    # ------------------------------
    # 数据库连接配置
    # ------------------------------
    SQLALCHEMY_DATABASE_URI = BaseConfig.MYSQL_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    # ------------------------------
    # 数据库连接配置
    # ------------------------------
    SQLALCHEMY_DATABASE_URI = BaseConfig.MYSQL_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_mapping = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}




