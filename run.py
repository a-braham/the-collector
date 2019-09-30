import os

from app.app import create_app

env_name = os.getenv('FLASK_ENV')
env_port = os.getenv('FLASK_RUN_PORT')
app = create_app(env_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=(env_port or 5000))
