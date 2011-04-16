# coding: utf8

class TestMapper(object):

    def test_command(self, params):
        return {'command':'ok'}

    def get(self, key):
        return self.test_command


class Common(object):

    mapper = TestMapper()
