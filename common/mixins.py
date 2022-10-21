#!/usr/bin/env python
# coding=utf-8
from datetime import date, timedelta

from sqlalchemy.orm import exc as sqlalchemy_exc
from sqlalchemy.exc import IntegrityError
from flask import current_app
from common.extensions import db


class SQLExecuteError(Exception):
    pass


class DBMixin(object):
    # __table_args__ = {'extend_existing': True}

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    def update(self, commit=True, **kwargs):
        for attr, value in iter(kwargs.items()):
            setattr(self, attr, value)
        return self.save() if commit else self

    def save(self, commit=True):
        try:
            db.session.add(self)
            if commit:
                db.session.commit()
            return self
        except IntegrityError:
            if current_app.config['DEBUG']:
                raise IntegrityError
            db.session.rollback()
            raise SQLExecuteError("Save or update {} Fail, Id is {}".format(self.__class__, self.id))

    def commit(self):
        db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    @classmethod
    def get_or_create(cls, defaults=None, **kwargs):
        try:
            return db.session.query(cls).filter_by(**kwargs).one(), False
        except sqlalchemy_exc.NoResultFound:
            if defaults:
                kwargs.update(defaults)
            instance = cls(**kwargs)
            try:
                db.session.add(instance)
                db.session.flush()
                return instance, True
            except IntegrityError:
                db.session.rollback()
                return db.session.query(cls).filter_by(**kwargs).one(), True


def date_time(value, name):
    try:
        start_at = list(map(lambda x: int(x), value.split("-")))
        start = date(year=start_at[0], month=start_at[1], day=start_at[2])
        if 'end' in name:  # 结束时间需要加一天
            day1 = timedelta(days=1)
            start += day1
    except Exception as e:
        raise ValueError(f"{name}时间格式错误 例:2022-01-01【{e}】")
    return start
