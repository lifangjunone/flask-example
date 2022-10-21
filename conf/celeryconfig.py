import celery
from conf.config import BaseConfig

is_version_new = False
print(celery.version_info >= (5, 2))
if celery.version_info >= (5, 2):
    is_version_new = True


if is_version_new:
    broker_url = BaseConfig.BROKER_URL
    result_backend = BaseConfig.RESULT_BACKEND
    result_serializer = 'json'
    accept_content = ['json', 'msgpack', 'yaml']
    result_expires = 1800
    task_serializer = 'json'
else:
    BROKER_URL = BaseConfig.BROKER_URL
    CELERY_RESULT_BACKEND = BaseConfig.RESULT_BACKEND
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
    CELERY_TASK_RESULT_EXPIRES = 1800
    CELERY_TASK_SERIALIZER = 'json'
