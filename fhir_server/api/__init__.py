from flask import Blueprint

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

from .identification_routes import *  # noqa
from .base_routes import *  # noqa
