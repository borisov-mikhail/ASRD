from flask import Flask
from flask_basicauth import BasicAuth
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import asrd.config as conf

app = Flask(__name__)
app.secret_key = conf.SECRET_KEY
app.config['BASIC_AUTH_USERNAME'] = conf.BASIC_AUTH_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = conf.BASIC_AUTH_PASSWORD
app.config['SQLALCHEMY_DATABASE_URI'] = conf.SQLALCHEMY_DATABASE_URI
app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'] = conf.SQLALCHEMY_TRACK_MODIFICATIONS

basic_auth = BasicAuth(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from asrd import database
