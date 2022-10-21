#!/usr/bin/env python
# coding=utf-8

import logging
from flask_restful import Resource

_logger = logging.getLogger(__name__)


class HealthCheck(Resource):
    def get(self):
        """
        This function is used to say current status to the Consul.
        Format: https://www.consul.io/docs/agent/checks.html

        Returns: Empty response with status 200, 429 or 500
        """
        # TODO: implement any other checking logic.
        # _logger.info('Health status: Bad')
        # _logger.warning('Health status: concerning')
        return '', 200
