#!/usr/bin/env python
# coding=utf-8

import pytest
import gevent

import gevent.monkey

gevent.monkey.patch_all()


def foo(i):
    print('Running in foo' + str(i))
    gevent.sleep(1)
    print('Explicit context switch to foo again')


tasks = [gevent.spawn(foo, i) for i in range(0, 5)]
gevent.joinall(tasks)
