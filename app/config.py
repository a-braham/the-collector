import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

class Config(object):
    """
    A configuration class that contains default config variables
    """
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    ACCESS_SECRET = os.getenv('ACCESS_SECRET')

class Production(Config):
    """
    A configuration class that contains config envs for production
    """
    DEBUG = False

class Development(Config):
    """
    A configuration class that contains config envs for development
    """
    DEBUG = True

class Testing(Config):
    """
    A configuration class that contains config envs for testing
    """
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')

app_config = {
    'production': Production,
    'development': Development,
    'testing': Testing
}
