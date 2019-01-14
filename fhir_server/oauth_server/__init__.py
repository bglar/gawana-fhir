from flask import Blueprint

from fhir_server.configs import DefaultConfig

api_auth = Blueprint("api_auth", __name__, url_prefix="")
api_auth.config = DefaultConfig.OAUTH2_CONFIG

from .models import *  # noqa
from .urls import *  # noqa
