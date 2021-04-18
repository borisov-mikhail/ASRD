from flask import Flask
from flask_basicauth import BasicAuth

import asrd.config as conf

app = Flask(__name__)
app.secret_key = conf.SECRET_KEY

app.config['BASIC_AUTH_USERNAME'] = conf.BASIC_AUTH_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = conf.BASIC_AUTH_PASSWORD

app.config['SQLALCHEMY_DATABASE_URI'] = conf.SQLALCHEMY_DATABASE_URI
app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'] = conf.SQLALCHEMY_TRACK_MODIFICATIONS

basic_auth = BasicAuth(app)

# Because the Flask is fuck tool,
# and can not init app without transitive dependencies
import asrd.database
import asrd.routes
