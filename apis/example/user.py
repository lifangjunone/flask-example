import logging

from flask_restful import Resource, request
from common.return_data import get_return_data, Success, Unsuccessfully
from apis.models.user import User
from apis.schemas.user import UserSchema
import json


class UserViewSet(Resource):

    def get(self):
        user = User.query.filter(User.is_delete==False).all()
        user_info = UserSchema().dumps(user, many=True)
        return get_return_data(Success, json.loads(user_info))

    def post(self):
        data = json.loads(request.data)
        user = User.create(**data)
        data = UserSchema().dumps(user)
        return get_return_data(Success, json.loads(data))

    def delete(self):
        try:
            id = json.loads(request.args.get("id"))
            user = User.query.get(id)
            user.is_delete = True
            user.save()
            return get_return_data(Success, {})
        except Exception as e:
            print(str(e))
            return get_return_data(Unsuccessfully, {}, msg=str(e))

    def put(self):
        data = json.loads(request.data)
        user_id = data.get("id")
        try:
            user = User.query.get(user_id)
            user.username = data.get("username")
            user.age = data.get("age")
            user.sex = data.get("sex")
            user.save()
            data = UserSchema().dumps(user)
            return get_return_data(Success, json.loads(data))
        except Exception as e:
            print(str(e))
            return get_return_data(Unsuccessfully, {}, msg=str(e))
