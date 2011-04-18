# coding: utf8
import time
import unittest
import logging

logging_frm = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging_level = logging.DEBUG
logging.basicConfig(format=logging_frm, level=logging_level)

class TestCase(unittest.TestCase):

    def wait_equal(self, attr, expected):
        MAX_COUNT = 30
        count = 0

        def param():
            if callable(attr):
                return attr()
            else:
                return attr

        def do_assert():
            return self.assertEqual(param(), expected)

        while True:
            count += 1
            if param() == expected:
                return do_assert()
            if count >= MAX_COUNT:
                return do_assert()

            time.sleep(0.1)

def log_debug(f):

    def wrapper(obj, *args, **kwargs):
        logging.debug('%s - %s' % (obj, f.func_name))

        return f(obj, *args, **kwargs)

    return wrapper
