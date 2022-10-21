#!/usr/bin/env python
# coding=utf-8

import json

from flask_restful import abort
from flask_restful import fields
from flask_restful import reqparse


def check_json_format(raw_msg):
    try:
        js = json.loads(raw_msg, encoding='utf-8')
    except ValueError:
        return False, {}
    return True, js


def not_found_response(message='Resource doesn\'t exist'):
    abort(404, message)


def not_authorized_response(message='you\'r not authorized contact the admin'):
    abort(401, message)


def success_response(message='operation success'):
    return {'message': message}, 200


def created_response(message='operation success'):
    return {'message': message}, 201


def created_response_with_payload(payload):
    return payload, 201


def unable_to_process_response(errors):
    return errors, 400


paginate_fields = {
    'total': fields.Integer,
    'pages': fields.Integer,
    'per_page': fields.Integer,
    'page': fields.Integer,
    'has_next': fields.Boolean,
    'has_prev': fields.Boolean,
    'next_num': fields.Integer,
    'prev_num': fields.Integer,
}

paginageParser = reqparse.RequestParser()
paginageParser.add_argument('page', type=int, default=1)
paginageParser.add_argument('limit', type=int, default=10)
