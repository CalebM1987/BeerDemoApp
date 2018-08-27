import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from flask import Flask, jsonify, url_for
from flask_cors import CORS, cross_origin
import urllib
from .exceptions import *
from .utils import *

__all__ = ('FlaskExtension', 'collect_args', 'jsonify')

# handlers for json exceptions
HANDLERS = [
    (InvalidCredentials, invalid_credentials),
    (UnauthorizedUser, unauthorized_user),
    (TokenRequired, token_required),
    (TokenExpired, token_expired)
]

class FlaskExtension(Flask):  # inherit from Flask object

    def __init__(self, *args, **kwargs):

        # call super class
        super(self.__class__, self).__init__(name)

        # wrap in CORS
        self.cors = CORS(self)
        self.config['CORS_HEADERS'] = 'Content-Type'

        # register error handlers
        self.handler = JSONExceptionHandler(self)
        for ex, h in HANDLERS:
            self.handler.register(ex, h)

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