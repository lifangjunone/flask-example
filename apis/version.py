#!/usr/bin/env python
# coding=utf-8

import platform

from flask_restful import Resource
from flask import current_app


class ApiVersion(Resource):
    def get(self):
        """
        API版本及环境信息
        :return: dict
        """
        result = {'api_version': 'v1',
                  'production': current_app.config['PROD_NAME'],
                  'app_version': current_app.config['CURRENT_VERSION'],
                  'application': current_app.config['SERVICE_NAME'],
                  'platform': platform.platform()}
        return result
