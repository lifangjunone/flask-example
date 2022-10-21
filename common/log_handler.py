#!/usr/bin/env python
# coding=utf-8

import os
import sys
import logging
import logging.handlers


class LogHandler:
    def __init__(self, app):
        self.create_logdir(app)

        root = logging.getLogger()
        log_format = '%(asctime)s %(levelname)s {prod_name} {service_name} {version} [%(filename)s:line:%(lineno)d] ' \
                     '%(message)s'.format(prod_name=app.config['PROD_NAME'], service_name=app.config['SERVICE_NAME'],
                                          version=app.config['CURRENT_VERSION'])
        # 日志标准格式
        logging_format = logging.Formatter(
            fmt=log_format)
        # 日志分割 (最大存储20个日志文件，每个文件100MB)
        rf_handler = logging.handlers.RotatingFileHandler(app.config['LOG_FILE'], maxBytes=1024 * 1024 * 100,
                                                          backupCount=20)
        # 设置日志信息输出的级别
        # 查看当前的日志级别：
        # logging.getLevelName(logger.getEffectiveLevel())
        # 小于指定级别的信息将被忽略
        rf_handler.setFormatter(logging_format)

        root.setLevel(app.config['GLOBAL_LOGLEVEL'])
        root.addHandler(rf_handler)
        # root.addHandler(logging.handlers.WatchedFileHandler(config.LOG_FILE))

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(app.config['GLOBAL_LOGLEVEL'])
        stream_handler.setFormatter(logging_format)
        root.addHandler(stream_handler)

        # 关闭wekzeug日志信息（与uWSGI日志相似产生冗余）
        log = logging.getLogger('werkzeug')
        log.disabled = True

    @staticmethod
    def create_logdir(app):
        # 创建日志目录
        try:
            os.makedirs(app.config['LOG_DIR_PREFIX'])
        except Exception as reason:
            pass
