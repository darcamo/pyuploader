# -*- coding: utf-8 -*-

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

from app import views, models
from app.views import admin
