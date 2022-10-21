#!/usr/bin/env python
# coding=utf-8

import unittest
from unittest import mock
from unittest.mock import patch

import pytest


# fixture，为可靠的和可重复执行的测试提供固定的基线
# 可以理解为测试的固定配置，使不同范围的测试都能够获得统一的配置，可以对这些基础设置设置初始化步骤以及析构步骤
#
# 比如所有test都需要连接同一个数据库，那可以设置为module，只需要连接一次数据库
# 这些重复的代码只需要在fixture中写一遍就好，同时fixture也可以指定scale（方法级，类级，模块级，session级）
#
# function：每个test都运行，默认是function的scope
# class：每个class的所有test只运行一次
# module：每个module的所有test只运行一次
# session：每个session只运行一次

@pytest.fixture(scope='function')
def setup_function(request):
    def teardown_function():
        print("teardown_function called.")

    request.addfinalizer(teardown_function)
    print('setup_function called.')


@pytest.fixture(scope='module')
def setup_module(request):
    def teardown_module():
        print("teardown_module called.")

    request.addfinalizer(teardown_module)
    print('setup_module called.')


def test_1(setup_function):
    print('Test_1 called.')


def test_2(setup_module):
    print('Test_2 called.')


def test_3(setup_module):
    print('Test_3 called.')


class Calculator(object):
    def add(self, a, b):
        return a + b


class TestProducer(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    @mock.patch.object(Calculator, 'add')
    def test_add(self, mock_add):
        mock_add.return_value = 3
        self.assertEqual(self.calculator.add(8, 14), 3)
