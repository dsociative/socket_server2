# coding: utf8

import sys
import traceback

def trace():
    traceback.print_exc(file=sys.stderr)

class Common(object):

    mapper = None
    policy_xml = '''<?xml version="1.0"?>
<!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy>
<allow-access-from domain="*" to-ports="*" secure="false" />
</cross-domain-policy>'''
