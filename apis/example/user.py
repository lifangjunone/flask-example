from flask_restful import Resource
from common.return_data import get_return_data, Success
from apis.models.user import User
from apis.schemas.user import UserSchema


class UserViewSet(Resource):

    def get(self):
        user = User.query.all()
        user_info = UserSchema().dumps(user, many=True)
        return get_return_data(Success, user_info)
