import random
import string
import os
import sys
import json
import six
from datetime import datetime, timedelta
thisDir = os.path.dirname(__file__)
sys.path.append(os.path.join(thisDir, 'lib'))
from flask import jsonify, Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import models
reload(models)
from models import Users, engine, Base
from sqlalchemy.orm import sessionmaker
import utils
reload(utils)
from utils import *

# make sure all databases are created
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

Users.query = session.query(Users)

# user fields to return
user_fields = ['id', 'name', 'username', 'email']

security_api = Blueprint('security_api', __name__)

__all__ = ('Users', 'security_api')

def create_random_string(length=64):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(length or 64)])

class UserStore(object):
    """helper class for user store"""

    @property
    def users(self):
        return session.query(Users).all()

    @property
    def active_tokens(self):
        return { u.token: u for u in session.query(Users).filter(Users.expires > datetime.now()).all() }

    def get_user(self, **kwargs): #id=None, username=None, email=None):
        try:
            return query_wrapper(Users, **kwargs)[0]
        except IndexError:
            return jsonify({'error': {'message': 'user not found'}})
        # if id:
        #     return session.query(Users, id=int(id)).first()
        #
        # elif username:
        #     return session.query(Users, username=username).first()
        #
        # elif email:
        #     return session.query(Users, email=email).first()


    def get_users(self, **kwargs):
        return query_wrapper(Users, **kwargs)

    def create_user(self, name, email, username, password):

        # create a token for this user, this hash is used by service to lookup user
        token = create_random_string()
        pw = generate_password_hash(password, salt_length=16)
        user = Users(name=name, email=email, username=username, password=pw, token=token)
        session.add(user)
        session.commit()
        # return { 'token': token, 'expires': user.expires }
        return user

    def check_user(self, username, password):
        user = self.get_user(username=username)
        if not user:
            return None
        return user if check_password_hash(user.password, password) else None


userStore = UserStore()


@security_api.route('/users')
@security_api.route('/users/<id>')
def get_users(id=None):
    if id:
        user = query_wrapper(Users, id=int(id))
        return jsonify(to_json(user, user_fields))

    # check for args and do query
    args = collect_args()
    results = query_wrapper(Users, **args)
    return jsonify(to_json(results, user_fields))

@security_api.route('/users/create', methods=['POST'])
def create_user():
    args = collect_args()
    try:
        userStore.create_user(**args)
        return jsonify({'success': 'successfully created user: {}'.format(args.get('username'))})
    except Exception as e:
        return jsonify({'error': {'message': 'could not create user', 'code': str(e)}})

@security_api.route('/users/login', methods=['POST'])
def login():
    args = collect_args()
    username = args.get('username')
    password = args.get('password')
    remember_me = args.get('remember', False) in ('true', True)
    print('remember me: ', remember_me)
    validatedUser = userStore.check_user(username, password)
    if validatedUser:
        login_user(validatedUser, remember=remember_me)
        validatedUser.last_login = datetime.utcnow()
        session.commit()
        return jsonify({'success': 'user logged in', 'token': validatedUser.token})
    return jsonify({'error': {'message': 'login error'}})

@security_api.route('/users/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
    except Exception as e:
        return jsonify({'error': {'message': str(e)}})
    return jsonify({'success': 'successfully logged out'})

@security_api.route('/security/test')
@login_required
def sec_test():
    return jsonify({'success': 'passed security'})