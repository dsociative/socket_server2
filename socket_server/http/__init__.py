# coding: utf8

from http_socket import WebClient

def web_only(f_exec):

    def wrapper(object, *args, **kwargs):

        if not isinstance(object.client, WebClient):
            return object.msg.error('only for web request')

        return f_exec(object, *args, **kwargs)

    return wrapper


