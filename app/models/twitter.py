from . import db
from marshmallow import Schema, fields

class TwitterModel(db.Model):
    """
    A model for tweets fetched from twitter
    """
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    tweeter_id =  db.Column(db.Integer, db.ForeignKey('tweeters.id'), nullable=False)
    tweet = db.Column(db.String(length=None), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    reply = db.relationship('ReplyModel', backref='tweets', lazy=True)    

    def __init__(self, data):
        self.tweeter_id = data.get('tweeter_id')
        self.tweet = data.get('tweet')
        self.type = data.get('type')

    def save(self):
        db.session.add(self)
        db.session.commit()

class TwitterSchema(Schema):
    """
    A schema class for twitter data
    """
    tweet = fields.String(required=True)

class ReplyModel(db.Model):
    """
    A model for replies made by the user for a tweet
    """
    __tablename__ = 'replies'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tweeter_id = db.Column(db.Integer, db.ForeignKey('tweeters.id'), nullable=False)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'), nullable=False)
    reply = db.Column(db.String(length=None), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.tweeter_id = data.get('tweeter_id')
        self.tweet_id = data.get('tweet_id')
        self.tweet = data.get('reply')

    def save(self):
        db.session.add(self)
        db.session.commit()

class ReplySchema(Schema):
    """
    A schema for replies made by users
    """
    user_id = fields.Integer(required=True)
    tweeter_id = fields.Integer(required=True)
    tweet_id = fields.Integer(required=True)
    tweet = fields.String(required=True)
