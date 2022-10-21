#!/usr/bin/env python
# coding=utf-8
import time

from common.extensions import celery


@celery.task()
def calc_sum(nums):
    """
    Call example: calc_sum.delay([1, 2, 3, 4, 5])
    calc sum
    :param nums: [1, 2, 3, 4, 5]
    :return:
    """
    return sum(nums)


