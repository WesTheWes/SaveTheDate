import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_SSL = True
    MAIL_SUBJECT_PREFIX = '[KaplanEverAfter] '
    MAIL_SENDER = 'Gina And Wes Kaplan <GinaAndWes@KaplanEverAfter.com>'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    SERVER_NAME = 'localhost:5000'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SERVER_NAME = os.environ.get('SERVER_NAME')

config = {
    'developement' : DevelopmentConfig,
    'production' :ProductionConfig,

    'default' : DevelopmentConfig
}