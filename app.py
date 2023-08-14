from flask import *
from flask_migrate import Migrate,MigrateCommand
from apps import create_app
from flask_script import Manager
from models import *

app = create_app()
manager = Manager(app=app)
migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    #app.run()
    manager.run()