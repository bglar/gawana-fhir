from http.client import HTTPException

from flask import render_template
from sqlalchemy_utils import register_composites
from flask_api import FlaskAPI
from flask_api.app import urlize_quoted_links, APISettings

import redis
from celery import Celery

from fhir_server.configs.database import db
from fhir_server.resources import *
from fhir_server.api import response as Response
from fhir_server.api import *  # noqa
from fhir_server.api.url_converters import FhirOperationsConverter
from fhir_server.oauth_server import *  # noqa
# from fhir_server.resources.profiledOrg import DemoOrgResource1

from .configs import *  # noqa

basedir = os.path.abspath(os.path.dirname(__file__))

my_resources = Blueprint(
    'flask-api', __name__,
    url_prefix='/flask-api',
    template_folder='templates', static_folder='static'
)


class FhirAPI(FlaskAPI):
    def __init__(self, *args, **kwargs):
        super(FlaskAPI, self).__init__(*args, **kwargs)
        self.api_settings = APISettings(self.config)
        self.register_blueprint(my_resources)
        self.jinja_env.filters['urlize_quoted_links'] = urlize_quoted_links


# For import *
__all__ = ['create_app']

DEFAULT_BLUEPRINTS = [
    api_v1,
    api_auth
]


def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = DefaultConfig.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = FhirAPI(app_name)
    configure_app(app, config)

    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
    app.config['CACHE_TYPE'] = 'redis'
    app.config['TRAP_HTTP_EXCEPTIONS'] = True
    app.config['DEFAULT_RENDERERS'] = [
        'flask_api.renderers.JSONRenderer',
        'flask_api.renderers.BrowsableAPIRenderer',
    ]
    app.config['DEFAULT_PARSERS'] = [
        'flask_api.parsers.JSONParser',
        'flask_api.parsers.URLEncodedParser',
        'flask_api.parsers.MultiPartParser'
    ]
    app.config.from_object(os.environ['APP_SETTINGS'])

    db.init_app(app)
    configure_extensions(app)
    configure_blueprints(app, blueprints)

    if not app.config['DEBUG']:
        # Override default Flask error handlers if DEBUG = False
        configure_error_handlers(app)

    db.app = app

    conn = db.session.connection()
    register_composites(conn)

    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Without this you get an extension not
        # registered error
        db.create_all()

    if app.debug:
        print('running in debug mode')
    else:
        print('NOT running in debug mode')
    return app


def configure_app(app, config=None):
    """Different ways of configurations."""

    app.config.from_object(DefaultConfig)

    if config:
        app.config.from_object(config)
        return

    MODE = os.getenv('APPLICATION_MODE', 'DEVELOPMENT')
    print("Running in %s mode" % MODE)
    app.config.from_object(get_config(MODE))


def configure_extensions(app):
    # register werkzeug routing converter
    app.url_map.converters['fhirop'] = FhirOperationsConverter

    # redis
    app.redis = redis.StrictRedis(
        host=app.config['REDIS_CONFIG']['HOST'],
        port=app.config['REDIS_CONFIG']['PORT'],
        db=app.config['REDIS_CONFIG']['CACHE_DB'])

    # Celery
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_error_handlers(app):
    # TODO: NOTE that line 97 of flask-api's base code has been changed to
    # typecast values for blueprint_handlers and app_handlers from tuple to
    # dict. This should be changed once a discussion at
    # https://github.com/tomchristie/flask-api/issues/61 has reach a
    # conclusion

    @app.errorhandler(Exception)
    def handle_errors(error):
        """
        A generic error handler to override Flask's default error handler.

        This intercepts all exceptions and errors and  logs them to an
        OperationOutcome resource.
        :param error:
        :return Operationoutcome resource instance:
        """

        diagnostics = error.__str__()
        try:
            return Response.log_operation_outcome(
                location=None, status_code=error.code, severity='fatal',
                diagnostics=diagnostics)

        except Exception as e:
            return Response.log_operation_outcome(
                location=None, status_code=500, severity='fatal',
                diagnostics=e)
