from flask import Blueprint
from flask_restful import Api

from .users import SignupView, LoginView
from .twitter import TwitterSearch, TwitterStream

bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp)

api.add_resource(SignupView, '/signup/')
api.add_resource(LoginView, '/login/')
api.add_resource(TwitterSearch, '/twitter/search')
api.add_resource(TwitterStream, '/twitter/stream')
