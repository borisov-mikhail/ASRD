import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
GRAPH_FOLDER = os.getenv('GRAPH_FOLDER')
UPLOAD_PATH = os.getenv('UPLOAD_PATH')
