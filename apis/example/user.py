from flask_restful import Resource


class UserViewSet(Resource):

    def get(self):
        user_info = {
            "name": "张三",
            "age": 22,
            "sex": "男"
        }
        return user_info
