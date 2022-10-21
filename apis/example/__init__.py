from flask_restful import Api
from flask import Blueprint

from .user import UserViewSet
from apis.version import ApiVersion

example_bp = Blueprint("example_api", __name__)
example_api = Api(example_bp, catch_all_404s=True)
example_api.add_resource(UserViewSet, "/user")
example_api.add_resource(ApiVersion, "/version")