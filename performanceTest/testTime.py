"""
记录时间
"""
import time


def testTime(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print('耗时：%s' % (end - start))

    return wrapper
