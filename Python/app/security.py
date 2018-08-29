import random
import string
from datetime import datetime
from flask import jsonify, Blueprint, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import models
reload(models)
from models import User, session
import utils
reload(utils)
from utils import *
from exceptions import *

# user fields to return
user_fields = ['id', 'name', 'username', 'email']

# create blue print
security_api = Blueprint('security_api', __name__)

__all__ = ('User', 'security_api', 'userStore', 'unauthorized_callback')

# unauthorized user callback for flask login (must return a Response() )
unauthorized_callback = lambda: json_exception_handler(UnauthorizedUser)

def create_random_string(length=64):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(length or 64)])

class UserStore(object):
    """helper class for user store"""

    @property
    def users(self):
        return session.query(User).all()

    def get_user(self, **kwargs):
        try:
            return query_wrapper(User, **kwargs)[0]
        except IndexError:
            raise UserNotFound

    def get_users(self, **kwargs):
        return query_wrapper(User, **kwargs)

    def create_user(self, name, email, username, password, activated='False'):

        # create a token for this user, this hash is used by service to lookup user
        token = create_random_string()
        pw = generate_password_hash(password, salt_length=16)
        user = User(name=name, email=email, username=username, password=pw, token=token, activated=activated)
        session.add(user)
        session.commit()
        return user

    def check_user(self, username, password):
        user = self.get_user(username=username)
        if not user:
            return None
        return user if check_password_hash(user.password, password) else None

userStore = UserStore()

# API METHODS BELOW

@security_api.route('/error')
def error():
    """ test the JSON Exception Handler """
    raise TestException

@security_api.route('/auth/test')
@login_required
def auth_test():
    return success('congratulations, you\'re authenticated')

@security_api.route('/users')
@security_api.route('/users/<id>')
def get_users(id=None):
    return endpoint_query(User, user_fields, id)

@security_api.route('/users/create', methods=['POST'])
def create_user():
    args = collect_args()
    try:
        userStore.create_user(**args)
        return success('successfully created user: {}'.format(args.get('username')))
    except:
        raise CreateUserError

@security_api.route('/users/login', methods=['POST'])
def login():
    args = collect_args()
    # with open('./text1.txt', 'w') as f:
    #     f.write(args.__class__.__name__)
    print(args)
    username = args.get('username')
    password = args.get('password')
    remember_me = args.get('remember', False) in ('true', True)
    validatedUser = userStore.check_user(username, password)
    if validatedUser:
        login_user(validatedUser, remember=remember_me)
        validatedUser.last_login = datetime.utcnow()
        session.commit()
        return success('user logged in', token=validatedUser.token)
    raise InvalidCredentials

@security_api.route('/users/welcome')
@login_required
def welcome():
    return success('Welcome {}'.format(current_user.name))

@security_api.route('/users/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
    except Exception as e:
        raise UnauthorizedUser
    return success('successfully logged out')