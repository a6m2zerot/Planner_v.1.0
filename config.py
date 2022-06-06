import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    OAUTHLIB_INSECURE_TRANSPORT = '1'  # убрать для прода!
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    API_SERVICE_NAME = 'calendar'
    API_VERSION = 'v3'

    CLIENT_SECRETS_FILE = "client.json"
