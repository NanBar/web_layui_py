import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
    DEBUG = False
    ALLOW_UNSAFE_WERKZEUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    ALLOW_UNSAFE_WERKZEUG = True


class ProductionConfig(Config):
    DEBUG = False
    ALLOW_UNSAFE_WERKZEUG = False
