from functools import wraps
from flask import request
from .authenticators import Authentication
from app.models.users import UserModel

auth = Authentication()


class Validators(object):
    """
    Class for validations:
        - validate that a user is authenticated before action.
    """

    def requires_auth(self, roles=[]):
        """
        A decorator method to validate authentication
        - check if there is any roles supplied, If any restrict using roles.
        """
        def decorator(func):
            @wraps(func)
            def decorator_func(*args, **kwargs):
                auth_token = None
                if 'Authorization' in request.headers:
                    auth_token = request.headers.get('Authorization')
                if not auth_token:
                    return {
                        'status': 401,
                        'message': 'Token required for authentication'
                    }, 401
                token = auth_token.split()[1]
                try:
                    resp = auth.verify_token(token)
                    if isinstance(resp, str):
                        user = UserModel.query.filter_by(username=resp).first()
                        if not user:
                            return {
                                'status': 400,
                                'message': 'Authentication failure'
                                }, 400
                except Exception as e:
                    return {
                        'status': 401,
                        'message': 'Invalid token, please login'
                        }, 400
                return func(user, **kwargs)
            return decorator_func
        return decorator
