from werkzeug.exceptions import HTTPException


class InvalidCredentials(HTTPException):
    code = 403
    name = 'Invalid Credentials'
    description = 'Invalid Credentials'
    message = 'Access Denied: Invalid Credentials'


class UnauthorizedUser(HTTPException):
    code = 401
    name = 'Unauthorized User'
    description = 'Unauthorized User'
    message = 'Access Denied: Unauthorized User'


class TokenRequired(HTTPException):
    code = 461
    name = 'Token Required'
    description = 'Token Required'
    message = 'Access Denied: a Token is required to access this resource'

class SessionExpired(HTTPException):
    code = 463
    name = 'Session Expired'
    description = 'Session Expired'
    message = 'Your session has expired, please login again'


class InvalidResource(HTTPException):
    code = 513
    name = 'Invalid Resource'
    description = 'Invalid Resource'
    message = 'The requested resource is invalid, please check the request parameters and try again'


class CreateUserError(HTTPException):
    code = 464
    name = 'Create User Error'
    description = 'Create User Error'
    message = 'Unable to create user, please check the input parameters and try again'


class UserNotFound(HTTPException):
    code = 465
    name = 'User Not Found'
    description = 'User Not Found'
    message = 'Could not find user'


class UserNotActivated(HTTPException):
    code = 466
    name = 'User Not Activated'
    description = 'User is not Activated'
    message = 'The user has not activated their account'

