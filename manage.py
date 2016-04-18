# -*- coding: utf-8 -*-

from flask.ext.script import Manager, Server, Shell
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db, models

manager = Manager(app)
# See http://blog.miguelgrinberg.com/post/flask-migrate-alembic-database-migration-wrapper-for-flask
# See this link to know how to migrate data
# https://julo.ch/blog/migrating-content-with-alembic/
migrate = Migrate(app, db)


# xxxxxxxxxx Commands xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Use 'python manage.py runserver' to run the flask development server
manager.add_command("runserver", Server())
# Use 'python manage.py runserver' to run the flask development server
manager.add_command("shell", Shell())
# Database migration commands
manager.add_command('db', MigrateCommand)
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


# @manager.command
# def create_db():
#     db.create_all()


@manager.shell
def make_shell_context():
    """
    Create a context for the shell. The shell will start with these
    variables already available.
    """
    return dict(app=app, db=db, models=models)


# xxxxxxxxxx Main xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
if __name__ == "__main__":
    manager.run()
