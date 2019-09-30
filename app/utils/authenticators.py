from datetime import datetime
from datetime import timedelta

import jwt

from app.config import Config

JWT_SECRET_KEY = Config.JWT_SECRET_KEY

class Authentication(object):
    """
    Authentication class handling:
        - Token generation
        - Token verifications
    """
    def generate_token(self, data):
        """
        method to generate authentication token
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=12000),
                'iat': datetime.utcnow(),
                'sub': data
            }
            return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')
        except Exception as e:
            return e
    
    def verify_token(self, token):
        """
        method to verify validity of the token
        """
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Token exppired, login again'
        except jwt.InvalidTokenError:
            return 'Invalid token, login'