from sqlalchemy import Column

from fhir_server.elements.base.complex_mixin import PgComposite
from fhir_server.elements import primitives
from fhir_server.elements.opentype import OpenType


class Extension(object):
    """ Optional Extensions Element - found in all resources. """

    def __call__(self, *args, **kwargs):
        return PgComposite(
            "fhir_extension",
            [
                Column("url", primitives.URIField, nullable=False),
                # identifies the meaning of the extension.
                Column("value", OpenType(), nullable=True),
            ],
        )


ElementExtension = Extension()
