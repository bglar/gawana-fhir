import re
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declared_attr
from flask_sqlalchemy import SignallingSession

from fhir_server.configs.database import db
from fhir_server.helpers.validations import validate_valuesets as vv
from fhir_server.elements import primitives
from fhir_server.elements.meta import MetaField
from fhir_server.utils import ElementSerializer, CRUDMixin, Versioned, versioned_session
from fhir_server.operations import BaseOperations


versioned_session(SignallingSession)
now = datetime.now(timezone.utc)
str_now = datetime.strftime(now, "%Y-%m-%dT%H:%M:%S%z")


class Resource(CRUDMixin, ElementSerializer, Versioned, BaseOperations, db.Model):
    """ Base Resource.

    This is the base resource type for everything.
    """

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__

    @declared_attr
    def meta(cls):
        # Metadata about the resource.
        return Column(MetaField())

    id = Column(
        primitives.IdField, default=lambda: uuid.uuid4().__str__(), primary_key=True
    )
    # Logical id of this artifact.

    implicitRules = Column(primitives.URIField)
    # A set of rules under which this content was created.

    language = Column(primitives.CodeField)
    # Language of the resource content.

    # =====================================================================
    # The Following fields are not in the fhir spec but have been added to
    # aid the implementation of certain concepts such as bringing deleted
    # resources back to life.
    # =====================================================================
    created_at = Column(primitives.InstantField, default=str_now)
    updated_at = Column(primitives.InstantField, default=str_now, onupdate=str_now)
    deleted_at = Column(primitives.InstantField, default=None)
    is_deleted = Column(primitives.BooleanField, default=False, index=True)

    # Add this as a resource attribute
    def validate_valuesets(self, value, url, resp):
        return vv(value, url, resp)

    def code_fields_validator(self, values, endpoint, message):
        if not values:
            return values

        if isinstance(values, list):
            for value in values:
                codes = value.get("coding")

                if codes:
                    # Avoid looping over `None` values
                    for code in codes:
                        code_val = code.get("code")
                        url = endpoint + "?code=" + code_val

                        self.validate_valuesets(code_val, url, message)

        elif isinstance(values, dict):
            codes = values.get("coding")
            if codes:
                for code in codes:
                    code_val = code.get("code")
                    url = endpoint + "?code=" + code_val

                    self.validate_valuesets(code_val, url, message)

        elif isinstance(values, str):
            url = endpoint + "?code=" + values
            self.validate_valuesets(values, url, message)

        return values

    def validate_references(self, reference, field_value):
        if reference and field_value:
            url_regex = (
                "((http|https):\/\/([A-Za-z0-9\\\/\.\-\:\%\$])*)?("
                + reference
                + ")\/[A-Za-z0-9\-\.]{1,64}(\/_history\/[A-Za-z0-9\-\.]{1,64})?"
            )
            pattern = re.compile(url_regex)

            if isinstance(field_value, list):
                for val in field_value:
                    if val.get("reference"):
                        if not pattern.fullmatch(val.get("reference")):
                            error = (
                                "The resource reference is not valid for {0} "
                                "field. Allowed resource references are {1}"
                            ).format(val, reference)
                            raise ValueError(error)
            else:
                if field_value.get("reference"):
                    if not pattern.fullmatch(field_value.get("reference")):
                        error = (
                            "The resource reference is not valid for {0} field."
                            "Allowed resource references are {1}"
                        ).format(field_value, reference)
                        raise ValueError(error)
