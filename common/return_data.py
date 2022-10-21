#!/usr/bin/env python
# coding=utf-8

from abc import ABC, abstractmethod


class AbstractAction(ABC):
    """
    Define an abstract class for ReturnData
    """


class ReturnData(AbstractAction):
    """
    Define an parent for Return data
    """

    def __init__(self, data):
        self._data = data
        self._msg = None
        self._code = None

    def return_data(self):
        return {
            "msg": self._msg,
            "code": self._code,
            "data": self._data
        }


class Success(ReturnData):
    """
    success return data
    """

    def __init__(self, data, msg=None):
        """
        Init success params
        Args:
            data: return json data
        """
        super().__init__(data)
        self._msg = msg if msg else "Successful"
        self._code = 10000


class Unsuccessfully(ReturnData):
    """
    success return data
    """

    def __init__(self, data, msg=None):
        """
        Init success params
        Args:
            data: return json data
        """
        super().__init__(data)
        self._msg = msg if msg else "Unsuccessfully"
        self._code = 10004


class UnsuccessfullyFileExist(ReturnData):
    """
    success return data
    """

    def __init__(self, data, msg=None):
        """
        Init success params
        Args:
            data: return json data
        """
        super().__init__(data)
        self._msg = msg if msg else "Unsuccessfully"
        self._code = 10101


class ParamError(ReturnData):
    """
    Param error return data
    """

    def __init__(self, data, msg=None):
        """
        Init param error params
        Args:
            data: return json data
        """
        super().__init__(data)
        self._msg = msg if msg else "Param is error"
        self._code = 10001


class ParamMissing(ReturnData):
    """
    Param missing return data
    """

    def __init__(self, data, msg=None):
        """
        Init param missing params
        Args:
            data:
        """
        super().__init__(data)
        self._msg = msg if msg else "Param is missing"
        self._code = 10002


class DataMissing(ReturnData):
    """
    DataMissing 没有查询到对应资源
    """

    def __init__(self, data, msg=None):
        """
        Init data missing params
        Args:
            data:
        """
        super().__init__(data)
        self._msg = msg if msg else "data is missing"
        self._code = 10003


class TokenInvalid(ReturnData):
    """
    TokenInvalid token 认证错误
    """

    def __init__(self, data, msg=None):
        """
        Init Invalid token
        Args:
            data:
        """
        super().__init__(data)
        self._msg = msg if msg else "TInvalid token"
        self._code = 10005


class PowerError(ReturnData):
    """
    Power error 权限错误
    """

    def __init__(self, data, msg=None):
        """
        Power error
        Args:
            data:
        """
        super().__init__(data)
        self._msg = msg if msg else "Power error"
        self._code = 10006


class TopNumError(ReturnData):
    """
    TopNum error 最大值错误
    """

    def __init__(self, data, msg=None):
        """
        TopNum error
        Args:
            data:
        """
        super().__init__(data)
        self._msg = msg if msg else "TopNum error"
        self._code = 10007


class ResourcesNotEnough(ReturnData):
    """
    resources not enough  资源不足
    """

    def __init__(self, data, msg=None):
        """
        resources not enough
        Args:
            data:
        """
        super().__init__(data)
        self._msg = msg if msg else "resources not enough"
        self._code = 10008


def get_return_data(return_class, data, msg=None):
    """
    Simple factory methods are used to produce return value objects
    Args:
        return_class:  Response class
        data: Response data
    Returns: return json object
    """
    return return_class(data, msg).return_data()


if __name__ == '__main__':
    """
    Call the example 
    """
    res = get_return_data(Success, {"name": "张三"})
    print(res)

