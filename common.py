# coding: utf8

class TestMapper(object):

    def test_command(self, params):
        return {'command':'ok'}

    def get(self, key):
        return self.test_command


class Common(object):

    mapper = TestMapper()
    policy_xml = '''<?xml version="1.0"?>
<!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy>
<allow-access-from domain="*" to-ports="*" secure="false" />
</cross-domain-policy>'''
