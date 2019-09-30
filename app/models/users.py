from . import db
from marshmallow import Schema, fields
from werkzeug.security import generate_password_hash

class UserModel(db.Model):
    """
    Model for users of the API
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=True)
    password =  db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    reply = db.relationship('ReplyModel', backref='users', lazy=True)

    def __init__(self, data):
        self.username = data.get('username')
        self.name = data.get('name')
        password = generate_password_hash(data.get('password'))
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()


class SignupSchema(Schema):
    """
    A schema for api users
    """
    username = fields.String(required=True)
    name = fields.String(allow_none=True)
    password = fields.String(required=True)

class LoginSchema(Schema):
    """
    A schema for api users
    """
    username = fields.String(required=True)
    password = fields.String(required=True)

class TwitterUserModel(db.Model):
    """
    Model for users of the API
    """
    __tablename__ = 'tweeters'
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    tweet = db.relationship('TwitterModel', backref='tweeters', lazy=True)
    reply = db.relationship('ReplyModel', backref='tweeters', lazy=True)

    def __init__(self, data):
        self.id = data.get('user_id')
        self.username = data.get('username')
        self.name = data.get('name')

    def save(self):
        db.session.add(self)
        db.session.commit()

class TwitterUserSchema(Schema):
    """
    A schema for twitter users
    """
    user_id = fields.Integer(required=True)
    username = fields.String(required=True)
    name = fields.String(allow_none=True)
