#!/usr/bin/env python
# coding=utf-8


def pytest_addoption(parser):
    parser.addoption('--host', action='store',
                     help='host of db')
    parser.addoption('--port', action='store', default='8888',
                     help='port of db')