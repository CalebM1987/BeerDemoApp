import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
import six
from flask import Flask, request, jsonify, current_app, Response, make_response, url_for
from flask.json import JSONEncoder
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import base64
import json
import urllib
from .exceptions import *
from .utils import *
from datetime import datetime, timedelta

VALID_CREDENTIALS = 'VALID_CREDENTIALS'
INVALID_CREDENTIALS = 'INVALID_CREDENTIALS'

__all__ = ('FlaskExtension', 'collect_args', 'jsonify')

# handlers
HANDLERS = [
    (InvalidCredentials, invalid_credentials),
    (UnauthorizedUser, unauthorized_user),
    (TokenRequired, token_required),
    (TokenExpired, token_expired)
]

class TokenSerializer(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return str(o)

class FlaskExtension(Flask):  # inherit from Flask object
    _app_kwargs = ('use_security', 'ldap_server', 'domain_name')

    def __init__(self, *args, **kwargs):
        # name, use_security=True, ldap_server=None, domain_name=None,
        if len(args):
            name = args[0]
        else:
            name = kwargs.get('name', __name__)
        app_kwargs = {k:v for k,v in six.iteritems(kwargs) if k in self._app_kwargs}

        # call super class
        super(self.__class__, self).__init__(name)

        # now add extra "FlaskExtension" specific arguments
        self.use_security = app_kwargs.get('use_security', True)
        self.sh = SecurityHandler(app_kwargs.get('ldap_server'), app_kwargs.get('domain_name'))

        # wrap in CORS
        self.cors = CORS(self)
        self.config['CORS_HEADERS'] = 'Content-Type'

        # register error handlers
        self.handler = JSONExceptionHandler(self)
        for ex, h in HANDLERS:
            self.handler.register(ex, h)

        # add genToken to mapping
        self.add_gen_token()

        # get token store directory
        self.token_store = os.path.join(os.path.dirname(__file__),'token_store', '{}.json'.format(name))
        if not os.path.exists(self.token_store):
            with open(self.token_store, 'w') as f:
                json.dump({'tokens': []}, f)

    @property
    def tokens(self):
        try:
            with open(self.token_store, 'r') as f:
                return json.load(f).get('tokens', [])
        except:
            return []

    def get_token(self):
        """gets a token if it exists"""
        header = 'AppToken'
        args = collect_args()
        token = None
        if args.get('token'):
            token = args.get('token')
        elif request.cookies.get('AppToken'):
            token = request.cookies['AppToken']
        elif request.headers.get(header):
            token = request.headers.get(header)
        return token

    def check_token(self, specific_users=[]):
        token = self.get_token()
        if not token:
            raise TokenRequired

        # loop through tokens to find match
        print 'checking token value: ', token
        for token_dict in self.tokens:
            print 'token_dict: ', token_dict
            if token == token_dict.get('token'):

                # make sure token is not expired
                if datetime.utcnow() > mil_to_date(token_dict.get('expires')):
                    raise TokenExpired

                # check for specific users
                if specific_users and token_dict.get('user') not in specific_users:
                    raise UnauthorizedUser

                return # exit method without exception

        # no token match
        raise UnauthorizedUser

    def authenticate(self, specific_users=[]):
        """decororator to validate security

        Optional:
            group -- group to validate token against in active directory, this is
                ignored if named_user param is set to True.
            named_user -- will authenticate against user store instead of Active Directory
                shen set to True. Default is False.
            specific_users -- list or comma separated string of specific users who can access
                resource.
        """
        def decorator(f):
            @wraps(f)   # functools.wraps
            @cross_origin(origin='*')
            def wrapped(*args, **kwargs):
                if self.use_security:  # check if security is enabled
                    self.check_token(specific_users) # custom method for validating token
                return f(*args, **kwargs)
            return wrapped
        return decorator

    def get_token_for_user(self, user):
        for t in self.tokens:
            if t.get('user') == user:
                return t
        return None

    def add_gen_token(self):

        # add genToken route
        @self.route('/genToken', methods=['POST'])
        def gen_token():

            # get arguments
            args = collect_args()
            usr = args.get('username', '')
            pw = base64.b64decode(args.get('password', ''))

            # validate against active directory
            status = self.sh.validate_AD(usr, pw)
            if status == INVALID_CREDENTIALS:
                raise InvalidCredentials

            # return token (just use werkzueg generate_password_hash to encrypt username)
            expires_time = datetime.utcnow() + timedelta(hours=8)
            expires = date_to_mil(expires_time)
            token = self.get_token_for_user(usr)
            new_token = False
            if not token:
                new_token = True
                token_str = generate_password_hash(usr, salt_length=32)
                token = {'token': token_str, 'expires': expires, 'user': usr}
            else:
                token['expires'] = expires

            # setup response object
            response = jsonify({'token': token.get('token'), 'expires': expires})

            # update token store
            toks = self.tokens
            if new_token:
                toks.append(token)
            else:
                # update token with new expiration
                for t in toks:
                    if t.get('token') == token.get('token'):
                        t['expires'] = expires

            # save back to token store
            with open(self.token_store, 'w') as f:
                json.dump({'tokens': toks}, f, indent=2)

            # set a cookie
            response.set_cookie('AppToken', value=token.get('token'), expires=expires_time)
            return response

        @self.route('/endpoints', methods=['GET', 'POST'])
        def endpoints():
            output = []
            for rule in self.url_map.iter_rules():

                options = {}
                for arg in rule.arguments:
                    options[arg] = "[{0}]".format(arg)

                methods = ','.join(rule.methods)
                url = url_for(rule.endpoint, **options)
                output.append({'function': rule.endpoint, 'methods': methods, 'url': urllib.unquote(url)})
            return jsonify({'endpoints': sorted(output, key=lambda d: d.get('url'))})

