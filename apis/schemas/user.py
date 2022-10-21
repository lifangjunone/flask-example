from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("is_delete",)

