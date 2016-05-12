# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.babel import Babel
from flask.ext.login import LoginManager
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.bower import Bower

# xxxxxxxxxx App Initialization xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
app = Flask(__name__)
Bower(app) # This provides the /bower url route.
try:
    # If config.py does not exist an exception is raised. We will create
    # config.py from default_config.py and try to load from the new config.py
    #  file.
    app.config.from_object('config')
except Exception:
    import os, binascii
    fid = open("default_config.py")
    fid2 = open("config.py", mode='w')
    data = fid.read()
    # Copy default_config.py to the new config.py file, but replace variables
    #  first.
    fid2.write(data.replace("MY_SUPER_SECRET_KEY_REPLACE_THIS",
                            binascii.hexlify(os.urandom(24)).decode('utf-8')))
    fid.close()
    fid2.close()
    # Load configuration from the new config file.
    app.config.from_object('config')

app.wsgi_app = ProxyFix(app.wsgi_app)
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxx Translation Support xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
babel = Babel(app)
# Set language to pt_BR so that the default error messages are translated
# in portuguese
app.config['BABEL_DEFAULT_LOCALE'] = 'pt_BR'
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxx Jinja2 Setup xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
app.jinja_env.trim_blocks = True
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxx Login xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'LoginView:logar'
lm.login_message = 'Você precisa logar para poder acessar essa página.'

# oid = OpenID(app, os.path.join(basedir, 'tmp'))
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxx Logging with Rotating File Setup xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LOG_FILE = app.config.get('LOG_FILE')
# Check if LOG_FILE is in a directory. In that case, create that directory if
#  necessary.
LOG_DIR = os.path.split(LOG_FILE)[0]
if LOG_DIR != "" and not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

# Now we create our rotating logger
handler = RotatingFileHandler(
    app.config.get('LOG_FILE'), maxBytes=10000, backupCount=5)
handler.setLevel(logging.DEBUG)
handler.setFormatter(
    logging.Formatter(
        fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s',
        datefmt='%b %d %H:%M:%S')
)
app.logger.addHandler(handler)
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxx Debug Toolbar xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
toolbar = DebugToolbarExtension(app)
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxx Database xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# When we initialize our app we also need to initialize our database.
db = SQLAlchemy(app)
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

from . import views, models
from .views import admin
