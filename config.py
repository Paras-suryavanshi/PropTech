import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# get the absolute path of the root directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # security and db
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-dev-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'proptech.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Max file size 5MB
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024