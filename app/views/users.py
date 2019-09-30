from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.security import check_password_hash
from app.models.users import UserModel, SignupSchema, LoginSchema
from app.utils.authenticators import Authentication
from app.models.twitter import ReplyModel
from app.models import db

signup = SignupSchema()
login = LoginSchema()
auth = Authentication()


class SignupView(Resource):
    """
    The signup view: Users need to be in the tool be able to send
    requests in the applications.
    """

    def post(self):
        try:
            json_data = request.get_json()
            data = signup.load(json_data)
        except ValidationError as error:
            return {'status': 400, 'message': error.messages}, 400

        username = data.get('username')
        user = UserModel.query.filter_by(username=username).first()
        if user:
            return {'status': 400, 'message': 'Username taken'}, 400
        user = UserModel(data)
        user.save()
        user = signup.dump(user)
        return {'status': 201, 'user': user}, 201


class LoginView(Resource):
    """
    The login view: A user needs to login to request data from twitter
    """

    def post(self):
        try:
            json_data = request.get_json()
            data = login.load(json_data)
        except ValidationError as error:
            return {'status': 400, 'message': error.messages}, 400
        username = data.get('username')
        user = UserModel.query.filter_by(username=username).first()
        records = UserModel.query.join(ReplyModel, ReplyModel.user_id == UserModel.id).all()
        print(records)
        if user and check_password_hash(user.password, json_data['password']):
            token = auth.generate_token(username)
            user = login.dump(user)
            return {'status': 200, 'user': user, 'token': token}, 200
        return {'status': 401, 'message': 'Incorrect credentials'}, 401
