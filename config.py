
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'local-development-only')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '1025'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'support@tickette.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')

    MAX_CONTENT_LENGTH = 4 * 1024 * 1024

    PROFILE_DIR = os.path.join(
        BASE_DIR, 'app/static/uploads/profiles'
    )


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql://admin:admin@127.0.0.1:3307/tickette'
    )


class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
