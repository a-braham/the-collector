import tweepy


class TweetListener(tweepy.StreamListener):
    """
    A handler for streaming tweets that match criteria provided.
    Objects: - Stream object gets tweets that match provided criteria
             - Stream listener to recieve the tweets.
    """

    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        return tweet

    def on_error(self, status):
        return 'Error dected'
