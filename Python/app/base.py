from flask import Flask, jsonify, url_for
from flask_cors import CORS
from werkzeug.exceptions import default_exceptions, HTTPException
import urllib
from .exceptions import *
from utils import *
import time

__all__ = ('FlaskExtension', 'collect_args', 'jsonify')

# handlers for json exceptions
HANDLERS = [(exc, json_exception_handler) for exc in (InvalidCredentials, UnauthorizedUser, TestException, TokenRequired, InvalidResource, CreateUserError)]

class JSONExceptionHandler(object):
    """https://coderwall.com/p/xq88zg/json-exception-handler-for-flask"""

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def std_handler(self, error):
        response = jsonify(message=error.message)
        response.status_code = error.code if isinstance(error, HTTPException) else 500
        return response

    def init_app(self, app):
        self.app = app
        self.register(HTTPException)
        for code, v in default_exceptions.iteritems():
            self.register(code)

    def register(self, exception_or_code, handler=None):
        self.app.errorhandler(exception_or_code)(handler or self.std_handler)

class FlaskExtension(Flask):  # inherit from Flask object

    def __init__(self, name, *args, **kwargs):

        # call super class
        super(self.__class__, self).__init__(name)

        # wrap in CORS for cross origin sharing
        self.cors = CORS(self)
        self.config['CORS_HEADERS'] = 'Content-Type'

        # register error handlers
        self.handler = JSONExceptionHandler(self)
        for ex, h in HANDLERS:
            self.handler.register(ex, h)

        # lookup for all endpoints
        @self.route('/endpoints', methods=['GET', 'POST'])
        def endpoints():
            output = []
            for rule in self.url_map.iter_rules():

                options = {}
                for arg in rule.arguments:
                    options[arg] = "[{0}]".format(arg)

                methods = ','.join(rule.methods)
                url = url_for(rule.endpoint, **options)
                output.append({'methods': methods, 'url': urllib.unquote(url)})
            return jsonify({'endpoints': sorted(output, key=lambda d: d.get('url'))})

    @staticmethod
    def get_timestamp():
        return time.strftime('%Y%m%d%H%M%S')