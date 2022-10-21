from flask_restful import Resource
from common.return_data import get_return_data, Success
import json


class UserViewSet(Resource):

    def get(self):
        user_info = {
            "name": "admin",
            "age": 22,
            "sex": "man"
        }
        return get_return_data(Success, user_info)
