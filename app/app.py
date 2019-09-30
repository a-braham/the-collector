from flask import Flask

from .config import app_config
from .models import db
from .views import bp

def create_app(env_name):
    """
    Create app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[env_name])
    app.url_map.strict_slashes = False

    app.register_blueprint(bp)

    db.init_app(app)

    return app
