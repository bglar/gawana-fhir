import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BaseConfig(object):
    PROJECT = "app"

    # Get app root path, also can use flask.root_path.
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    DEBUG = False
    USE_EMAIL = True
    TESTING = False
    PROD = False

    ADMINS = ['brian.ogollah@gmail.com']

    # for session
    SECRET_KEY = '172bb977-e752-4831-8959-2b87d1006669'
    DOMAIN_NAME = 'localhost:5000'
    API_ROOT = 'api'


class DefaultConfig(BaseConfig):
    SITE_NAME = "GawanaFhirServer"

    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '172bb977-e752-4831-8959-2b87d1006669'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    # redis
    REDIS_CONFIG = {
        'HOST': 'TEST_REDIS_HOST',
        'PORT': '2953',
        'CELERY_DB': '0',
        'CACHE_DB': '1'
    }

    # celery config
    CELERY_BROKER_URL = 'redis://%s:%s/0' % (
        REDIS_CONFIG['HOST'], REDIS_CONFIG['PORT']
    )
    CELERY_RESULT_BACKEND = 'redis://%s:%s/0' % (
        REDIS_CONFIG['HOST'], REDIS_CONFIG['PORT']
    )
    CELERY_RESULT_ENGINE_OPTIONS = {
        "pool_recycle": 7200, 'echo': True
    }

    # Oauth2
    OAUTH2_CONFIG = {
        'OAUTH2_PROVIDER_TOKEN_EXPIRES_IN': 3600
    }


class ProductionConfig(DefaultConfig):
    DEBUG = False


class StagingConfig(DefaultConfig):
    DOMAIN_NAME = 'localhost:5000'
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(DefaultConfig):
    DEVELOPMENT = True
    DEBUG = False


class TestingConfig(BaseConfig):
    DOMAIN_NAME = 'localhost:5000'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ['TEST_DATABASE_URL']


def get_config(MODE):
    SWITCH = {
        'DEVELOPMENT': DevelopmentConfig,
        'STAGING': StagingConfig,
        'PRODUCTION': ProductionConfig
    }

    return SWITCH[MODE]
