from sqlalchemy import Column
from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.orm import validates
from sqlalchemy_utils import CompositeArray as Array

from fhir_server.configs import (
    LOCATION_STATUS_URL,
    LOCATION_MODE_URL,
    SERVICE_DELIVERY_LOCATION_ROLE_TYPE_URL,
    LOCATION_PHYSICAL_TYPE_URI,
)
from fhir_server.elements import primitives, complex
from fhir_server.elements.base.backboneelement import BackboneElement
from fhir_server.resources.domainresource import DomainResource
from fhir_server.elements.base.complex_element import Field


class LocationPosition(BackboneElement):
    """ The absolute geographic location.

    The absolute geographic location of the Location, expressed using the WGS84
    datum (This is the same co-ordinate system used in KML).
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field(
                    "longitude", {"mini": 1, "maxi": 1}, primitives.DecimalField, None
                ),
                # Longitude with WGS84 datum.
                Field(
                    "latitude", {"mini": 1, "maxi": 1}, primitives.DecimalField, None
                ),
                # Latitude with WGS84 datum.
                Field("altitude", {"mini": 0, "maxi": 1}, primitives.DecimalField, None)
                # Altitude with WGS84 datum.
            ]
        )
        return elm


LocationPositionField = LocationPosition()


class Location(DomainResource):
    """ Details and position information for a physical place.

    Details and position information for a physical place where services are
    provided  and resources and participants may be stored, found, contained or
    accommodated.
    """

    identifier = Column(Array(complex.IdentifierField()))
    # Unique code or number identifying the location to its users.

    status = Column(primitives.CodeField)
    # active | suspended | inactive.

    name = Column(primitives.StringField)
    # Name of the location as used by humans.

    description = Column(primitives.StringField)
    # Description of the location.

    mode = Column(primitives.CodeField)
    # instance | kind.

    alias = Column(Array(primitives.StringField))
    # A list of alternate names that the location is known as,
    # or was known as in the past

    type = Column(complex.CodeableConceptField())
    # Type of function performed.

    telecom = Column(Array(complex.ContactPointField()))
    # Contact details of the location.

    address = Column(complex.AddressField())
    # Physical location.

    physicalType = Column(complex.CodeableConceptField())
    # Physical form of the location.

    position = Column(LocationPositionField())
    # The absolute geographic location.

    managingOrganization = Column(complex.ReferenceField())
    # Organization responsible for provisioning and upkeep.

    partOf = Column(complex.ReferenceField())
    # Another Location this one is physically part of.

    endpoint = Column(Array(complex.ReferenceField()))
    # Technical endpoints providing access to services
    # operated for the location

    @declared_attr
    def references(self):
        """
        :return:
        Dict. values in the dict should be a | separated string of
        reference resources"""

        return {"managingOrganization": "Organization", "partOf": "Location"}

    @validates("managingOrganization", "partOf")
    def reference_fields(self, key, field):
        """Validates multiple reference fields.

        To add more fields: @validates('field1', 'field2', 'field3')
        And replace the code block before the return statement with:
            ```
            for field_name, reference in self.references.items():
                if key == field_name:
                    self.validate_references(reference, field)
            ```
        """

        for field_name, reference in self.references.items():
            if key == field_name:
                self.validate_references(reference, field)

        return field

    @validates("status")
    def validate_location_status(self, key, status):
        msg = "location status"
        self.code_fields_validator(status, LOCATION_STATUS_URL, msg)

        return status

    @validates("mode")
    def validate_location_mode(self, key, mode):
        msg = "location mode"
        self.code_fields_validator(mode, LOCATION_MODE_URL, msg)

        return mode

    @validates("type")
    def validate_location_type(self, key, type):
        msg = "location type code"
        self.code_fields_validator(type, SERVICE_DELIVERY_LOCATION_ROLE_TYPE_URL, msg)

        return type

    @validates("physicalType")
    def validate_physical_type(self, key, physicalType):
        msg = "location physical type code"
        self.code_fields_validator(physicalType, LOCATION_PHYSICAL_TYPE_URI, msg)

        return physicalType

    def _resource_summary(self):
        summary_fields = ["id", "meta", "identifier", "name"]
        return {"repr": "%r" % self.name, "fields": summary_fields}

    def __repr__(self):
        return "<Location %r>" % self.name
