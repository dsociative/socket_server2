#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest2
import sys

if __name__ == '__main__':

    count = 0
    errors = 0
    fails = 0

    runner = unittest2.TextTestRunner()
    loader = unittest2.TestLoader()
    suites = loader.discover('socket_server/test', pattern='zt_*.py')
    for suite in suites:
        result = runner.run(suite)
        errors += len(result.errors)
        fails += len(result.failures)
        count += suite.countTestCases()

    runner.stream.writeln('%s tests, %s errors %s fails' % (count, errors,
                                                            fails))

    if errors or fails:
        sys.exit(1)
