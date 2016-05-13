
"""
Default Configuration for flask modules. Copy this file as 'config.py'
and change where required. You should at least change the SECRET_KEY value.

Note that you can get this configuration as app.config['CONFIG_NAME'].
Ex: app.config['SECRET_KEY']
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# xxxxxxxxxx Debug xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEBUG = True  # Debug will be activated with an argument to run method
DEBUG_TB_INTERCEPT_REDIRECTS = False  # Used by DebugToolbarExtension
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxx Configuration for the Flask-WTF extension xxxxxxxxxxxxxxxxxxxx
CSRF_ENABLED = True
# Activates the cross-site request forgery prevention (CSRF)
WTF_CSRF_ENABLED = True
# Generate a random secrete key. The SECRET_KEY setting is needed when CSRF
# is enabled in forms.
SECRET_KEY = 'MY_SUPER_SECRET_KEY_REPLACE_THIS'
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxx Logging xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LOG_FILE = os.path.join(basedir, 'log/app_logger.log')
LOG_DIR = os.path.split(LOG_FILE)[0]
if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxx SQL Configuration xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# The SQLALCHEMY_DATABASE_URI is required by the Flask-SQLAlchemy
# extension. This is the path of our database file.
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# The SQLALCHEMY_MIGRATE_REPO is the folder where we will store the
# SQLAlchemy-migrate data files.
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SQLALCHEMY_TRACK_MODIFICATIONS = False
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxx Upload Configuration xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
UPLOAD_FOLDER = 'app/uploads'
COURSE_NAME = 'ck179'
COURSE_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, COURSE_NAME)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
