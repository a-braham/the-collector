import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.app import create_app
from app.models import db

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
