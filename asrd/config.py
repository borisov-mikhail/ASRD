import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
UPLOAD_PATH = os.getenv('UPLOAD_PATH')
BASIC_AUTH_USERNAME = os.getenv('AUTH_USERNAME')
BASIC_AUTH_PASSWORD = os.getenv('AUTH_PASSWORD')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
