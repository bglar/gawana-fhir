from sqlalchemy import Column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates
from sqlalchemy_utils import CompositeArray as Array

from fhir_server.configs import ORGANIZATION_TYPE_URL
from fhir_server.elements import complex, primitives
from fhir_server.elements.base.backboneelement import BackboneElement
from fhir_server.resources.domainresource import DomainResource
from fhir_server.elements.base.complex_element import Field


class OrganizationContact(BackboneElement):
    """ Contact for the organization for a certain purpose.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('purpose', {'mini': 0, 'maxi': 1},
                  complex.CodeableConceptField(), None),
            # The type of contact.

            Field('name', {'mini': 0, 'maxi': 1},
                  complex.HumanNameField(), None),
            # A name associated with the contact.

            Field('address', {'mini': 0, 'maxi': 1},
                  complex.AddressField(), None),
            # Visiting or postal addresses for the contact.

            Field('telecom', {'mini': 0, 'maxi': -1},
                  complex.ContactPointField(), None)
            # Contact details (telephone, email, etc.)  for a contact.
        ])
        return elm


OrganizationContactField = OrganizationContact()


class Organization(DomainResource):
    """ A grouping of people or organizations with a common purpose.

    A formally or informally recognized grouping of people or organizations
    formed for the purpose of achieving some form of collective action.
    Includes companies, institutions, corporations, departments, community
    groups, healthcare practice groups, etc.
    """

    active = Column(primitives.BooleanField)
    # Whether the organization's record is still in active use.

    name = Column(primitives.StringField)
    # Name used for the organization.

    alias = Column(Array(primitives.StringField))
    # A list of alternate names that the organization is known as,
    # or was known as in the past

    identifier = Column(Array(complex.IdentifierField()))
    # Identifies this organization  across multiple systems.

    type = Column(complex.CodeableConceptField())
    # Kind of organization.

    partOf = Column(complex.ReferenceField())
    # The organization of which this organization forms a part.

    telecom = Column(Array(complex.ContactPointField()))
    # A contact detail for the organization.

    address = Column(Array(complex.AddressField()))
    # An address for the organization.

    endpoint = Column(Array(complex.ReferenceField()))
    # Technical endpoints providing access to services operated
    # for the organization

    contact = Column(Array(OrganizationContactField()))
    # Contact for the organization for a certain purpose.

    @declared_attr
    def references(self):
        """
        :return:
        Dict. values in the dict should be a | separated string of
        reference resources"""

        return {
            "partOf": "Organization",
            "endpoint": "Endpoint"
        }

    @validates('partOf', 'endpoint')
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

    @validates('type')
    def validate_organization_type(self, key, type):
        msg = 'organization type code'
        self.code_fields_validator(type, ORGANIZATION_TYPE_URL, msg)

        return type

    @validates('telecom')
    def validate_telecom(self, key, telecom):
        if telecom:
            for tel in telecom:
                code_val = tel.get('use')
                if code_val == 'home':
                    raise ValueError('The telecom of an organization '
                                     'can never be of use `home`')

        return telecom

    @validates('address')
    def validate_address(self, key, address):
        if address:
            for ad in address:
                code_val = ad.get('use')
                if code_val == 'home':
                    raise ValueError('An address of an organization can '
                                     'never be of use `home`')

        return address

    def _resource_summary(self):
        summary_fields = ['id', 'meta', 'identifier', 'name', 'type', ]
        return {
            'repr': '%r' % self.name,
            'fields': summary_fields
        }

    def __repr__(self):
        return '<%r %r>' % (self.__class__.__name__, self.name)
