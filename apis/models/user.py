from common.mixins import DBMixin, db
from common.db_mixins import DBMixins


class SexItem:
    """
    defined SexItem type
    """
    MAN = "男"
    WOMAN = "女"
    UNKNOWN = "未知"


class User(DBMixins, DBMixin):
    """
    ImageLibrary 影像信息
    """
    username = db.Column(db.String(255), nullable=True, comment="用户名")
    age = db.Column(db.Integer, default=0, comment="年龄")
    sex = db.Column(db.String(255), default=SexItem.MAN, comment="性别")
    is_delete = db.Column(db.Boolean, default=False)


