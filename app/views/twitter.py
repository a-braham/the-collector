from flask import request
import requests
from flask_restful import Resource
import tweepy
from marshmallow import ValidationError

from app.config import Config
from app.models.users import UserModel, TwitterUserModel
from app.models.twitter import TwitterSchema, TwitterModel, ReplyModel
from app.utils.validators import Validators
from app.utils.handlers import TweetListener

schema = TwitterSchema()
validate = Validators()

CONSUMER_KEY = Config.CONSUMER_KEY
CONSUMER_SECRET = Config.CONSUMER_SECRET
ACCESS_KEY = Config.ACCESS_KEY
ACCESS_SECRET = Config.ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)



class TwitterSearch(Resource):
    """
    View class to search twitter using key words passed by user
    Gather tweets based on key words provided
        This is a HTTP FlaskRestful method for fetching tweets based 
        on key words entered by the user.
        Events:- Search previous tweeets base on provided key words.
    """
    @validate.requires_auth
    def post(self):
        try:
            api.verify_credentials()
        except Exception as e:
            return{
                'error': {
                    'body': 'Authentication to Twitter API denied'
                }
            }, 401

        try:
            json_data = request.get_json()
            data = schema.load(json_data)
        except ValidationError as e:
            return {
                'error': {
                    'body': e.messages
                }
            }, 400

        key_word = data['tweet']

        tweets = []
        
        for tweet in api.search(q=key_word, lang='en', rpp=10):
            data = {
                'tweeter_id': tweet.user.id,
                'tweet': tweet.text,
                'type': 'SEARCH'
            }
            tweet = TwitterModel(data)
            tweet.save()
            data = schema.dump(tweet)
            tweets.append(data)

        import pdb; pdb.set_trace()
        return {
            'data': {
                'username': tweet.user.name,
                'tweet': tweet.text,
                'type': 'Search'
            }
        }


class TwitterStream(Resource):
    """
    View class to search twitter using key words passed by user
    Gather tweets based on key words provided
        This is a HTTP FlaskRestful method for fetching tweets based 
        on key words entered by the user.
        Events: - Listen for incoming tweets containing provided key words.
    """
    @validate.requires_auth
    def post(self):
        try:
            api.verify_credentials()
        except Exception as e:
            return{
                'error': {
                    'body': 'Authentication to Twitter API denied'
                }
            }, 401
        try:
            json_data = request.get_json()
            data = schema.load(json_data)
        except ValidationError as e:
            return {
                'error': {
                    'body': e.messages
                }
            }, 400

        key_word = data['tweet']
        listener = TweetListener(api)
        stream = tweepy.Stream(api.auth, listener)
        stream_filter = stream.filter(track=[key_word], lang=['en'])
        return("stream_filter")
        
