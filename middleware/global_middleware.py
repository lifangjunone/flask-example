

class RequestFilter(object):

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # print('request before pass RequestFilter')
        req = self.wsgi_app(environ, start_response)
        # print('request after pass RequestFilter')
        return req

