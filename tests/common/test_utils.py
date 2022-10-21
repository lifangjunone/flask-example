#!/usr/bin/env python
# coding=utf-8

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

import pytest

from common.utils import red


def add(a, b):
    """return a + b

    Args:
        a (int): int
        b (int): int

    Returns:
        a + b

    Raises:
        AssertionError: if a or b is not integer

    """
    assert all([isinstance(a, int), isinstance(b, int)])
    return a + b


def test_add():
    assert add(1, 2) == 3
    assert isinstance(add(1, 2), int)
    with pytest.raises(Exception):  # test exception
        add('1', 2)


def test_red():
    red_words = red('Ascii text color error.')
    print(red_words)
    assert red_words == '\033[31m\033[49m{0}\033[0m'.format('Ascii text color error.')
