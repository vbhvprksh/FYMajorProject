import os
from   os import environ

class Config(object):

    DEBUG = False
    TESTING = False
    
    basedir    = os.path.abspath(os.path.dirname(__file__))


    UPLOADS = "/home/username/app/app/static/uploads"

    SESSION_COOKIE_SECURE = True
    DEFAULT_THEME = None


class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    UPLOADS = "/home/username/app/app/static/uploads"
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    DEBUG = True

    UPLOADS = "/home/username/app/app/static/uploads"
    SESSION_COOKIE_SECURE = False


class DebugConfig(Config):
    DEBUG = False

