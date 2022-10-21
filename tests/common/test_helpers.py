#!/usr/bin/env python
# coding=utf-8
import random

import time

test_response = False

CONFIG_RETRY_TIME = 5
retry_time = 6
while retry_time < CONFIG_RETRY_TIME:
    next_sleep = random.random() * (2 ** retry_time)
    try:
        if test_response:
            print('success')
        else:
            print(next_sleep)
            time.sleep(next_sleep)
    except Exception:
        if retry_time >= CONFIG_RETRY_TIME - 1:
            raise
    retry_time += 1
