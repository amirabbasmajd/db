import os


def dot_secret():
    """
    This function will be used only if SECRET_KEY is not
    exported to environment.
    """
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DOT_SECRET = os.path.join(BASEDIR, '.secret_key')

    if os.path.exists(DOT_SECRET):
        with open(DOT_SECRET, 'r') as secret_file:
            secret_key = secret_file.read().strip()
        return secret_key


class Config():
    """
    Basic configuration class.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    WTF_CSRF_ENABLED = True
    PORTS = {
        'default': 465,
        'outlook': 587
    }
    HOSTS = {
        'yandex': 'smtp.yandex.ru',
        'outlook': 'smtp-mail.outlook.com',
        'gmail': 'smtp.gmail.com'
    }
    MAIL_SERVER = HOSTS.get('yandex')
    MAIL_PORT = PORTS.get('default')
    MAIL_SENDER = 'Admin <admin@example.com>'
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://localhost/enceladus'
    MONGO_DBNAME = os.environ.get('FLASK_MONGO_DB') or 'enceladus'


class TestConfig(DevelopmentConfig):
    MONGO_URI = 'mongodb://localhost/enceladus_test'
    MONGO_DBNAME = os.environ.get('FLASK_TEST_DB') or 'enceladus_test'


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'test': TestConfig
}
