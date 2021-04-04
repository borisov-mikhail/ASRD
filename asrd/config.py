import os

from dotenv import load_dotenv

load_dotenv()
basedir = '/home/mikhail/Development/asrd'

SECRET_KEY = os.getenv('SECRET_KEY')
UPLOAD_PATH = os.getenv('UPLOAD_PATH')
BASIC_AUTH_USERNAME = os.getenv('AUTH_USERNAME')
BASIC_AUTH_PASSWORD = os.getenv('AUTH_PASSWORD')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                          'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
