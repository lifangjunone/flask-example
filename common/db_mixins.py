from datetime import date, datetime

from sqlalchemy import text
from sqlalchemy.orm import exc as sqlalchemy_exc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect
from flask import current_app
from common.extensions import db


class SQLExecuteError(Exception):
    pass


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete)
    operations.
    """

    def _get_pk(self):
        """获取主键"""
        return inspect(self.__class__).primary_key[0].name

    def convert_to_dict(self, allow_list=None, filter_list=None):
        """把Object对象转换成Dict对象
        total_num 最多递归深度
        num 当前递归深度
        当 allow_list 不为空会只返回 allow_list 里面的属性
        filter_list过滤对应属性
        """
        filter_list = filter_list or ['password']
        if self is None:
            return {}
        dict_ = {}
        obj_keys_list = list(self._sa_class_manager.keys())
        for j in obj_keys_list:
            obj_value = self.__getattribute__(j)
            if obj_value in ["None", None]:
                obj_value = ""
            if allow_list and j not in allow_list:
                continue
            elif j in filter_list:
                continue
            elif not isinstance(obj_value, str) and not isinstance(obj_value, int) and not isinstance(obj_value, float):
                if isinstance(obj_value, datetime):
                    obj_value = str(obj_value)[:19]  # '2019-06-18 10:11:33.569000'
                else:
                    obj_value = str(obj_value)
            dict_[j] = obj_value
        return dict_

    @classmethod
    def all_to_dict(cls, obj):
        """将model-list 对象转换为字典"""
        data = []
        for c in list(obj):
            data.append(c.convert_to_dict())
        return data

    def save_data(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def set_data(self, is_save=False, **data):
        """ 赋值给models对象，model的增，改函数调用"""

        def _filter_build_in(keys):
            # 过滤obj的非数据库属性
            new_keys = list()
            for k in keys:
                if not k.startswith("_"):
                    new_keys.append(k)
            return new_keys

        attrs = _filter_build_in(dir(self))

        """将data设置值到record对象中"""
        for key in attrs:
            if key in data.keys():
                setattr(self, key, data[key])
        if is_save:  # 是否 add and commit
            self.save_data()

    @classmethod
    def all_set_data(cls, objs, data, is_save=False):
        """批量赋值"""
        for obj in list(objs):
            obj.set_data(is_save=is_save, **data)
        return list(objs)

    # @classmethod
    # def create_new(cls, **kwargs):
    #     """Create a new record and save it the database."""
    #     record = cls()
    #     record.set_data(is_save=True, **kwargs)
    #     return record.convert_to_dict()

    def update_data(self, **kwargs):
        """Update specific fields of a record."""
        # Prevent changing ID of object
        kwargs.pop('id', None)
        self.set_data(is_save=True, **kwargs)
        return self.convert_to_dict()

    def update_old(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        # Prevent changing ID of object
        kwargs.pop('id', None)
        for attr, value in kwargs.iteritems():
            # Flask-RESTful makes everything None by default :/
            if value is not None:
                setattr(self, attr, value)
        return commit and self.save() or self

    def delete_old(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()

    @classmethod
    def delete_data(cls, commit=True, **query_condition):
        """Remove the record from the database."""
        num = cls.query.filter_by(**query_condition).delete(synchronize_session=False)
        if commit:
            db.session.commit()
        return {"data": {"count": num}}

    @classmethod
    def select_list(cls, ilike=None, db_not=None, page=None, per_page=None, order_by=None,
                    ior_=None, iand_=None, start_at=None, end_at=None, max_per_page=100, **kwargs):
        """ """
        db_not = db_not or []  # 对应参数应该是个列表
        ilike = ilike or []
        ior_ = ior_ or []  # 示例 [{'key_name':id,'filter':'>=5'},{'key_name':id,'filter':'<=2'}]
        f = cls.query
        if start_at and end_at:
            start_at = start_at + " 00:00:00"
            end_at = end_at + " 23:59:59"
            start = datetime.strptime(start_at, '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(end_at, '%Y-%m-%d %H:%M:%S')
            f = f.filter(cls.created_at <= end).filter(cls.created_at >= start)
        else:
            if start_at:
                start_at = start_at + " 00:00:00"
                start = datetime.strptime(start_at, '%Y-%m-%d %H:%M:%S')
                f = f.filter(cls.created_at >= start)
            if end_at:
                end_at = end_at + " 23:59:59"
                end = datetime.strptime(end_at, '%Y-%m-%d %H:%M:%S')
                f = f.filter(cls.created_at <= end)

        if ior_:
            or_str = 'db.or_('
            for i in ior_:
                or_str += f"{cls.__name__}.{i['key_name']} {i['filter']},"
            f = f.filter(db.or_(eval(or_str)))
            or_str += ')'
            f = f.filter(eval(or_str))
        for i in kwargs:
            # api_log.info(i)
            if i in ilike:
                f = f.filter(getattr(cls, i).ilike('%{}%'.format(kwargs[i])))
            elif i in db_not:
                f = f.filter(db.not_(getattr(cls, i).in_(kwargs[i])))
            else:
                f = f.filter_by(**{i: kwargs[i]})
        if order_by:
            f = f.order_by(db.desc(order_by))
        return_data = {"data": []}
        if page and per_page:

            page = max(page, 1)
            per_page = min(per_page, max_per_page)
            per_page = max(per_page, 1)
            pagination = f.paginate(page, per_page, error_out=False)
            filter_ = pagination.items

            if filter_:
                return_data["data"] = filter_
                return_data['curr_page'] = pagination.page
                return_data['total_page'] = pagination.pages
                return_data['total'] = pagination.total
                return_data['page_size'] = pagination.per_page
                return return_data
        else:
            return return_data


class DBMixins(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    # updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    updated_at = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

