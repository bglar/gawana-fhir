from sqlalchemy import Column
from sqlalchemy_utils import CompositeArray as Array

from fhir_server.elements import (
    primitives, complex, Field, ComplexElement, ElementDefinitionField
)
from fhir_server.resources.domainresource import DomainResource


class StructureDefinitionContact(ComplexElement):
    """ Contact details of the publisher.

    Contacts to assist a user in finding and communicating with the publisher.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('name', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Name of a individual to contact.

            Field('telecom', {'mini': 0, 'maxi': -1},
                  complex.ContactPointField(), None)
            # Contact details for individual or publisher.
        ])
        return elm


StructureDefinitionContactField = StructureDefinitionContact()


class StructureDefinitionMapping(ComplexElement):
    """ External specification that the content is mapped to.

    An external specification that the content is mapped to.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('identity', {'mini': 1, 'maxi': 1},
                  primitives.IdField, None),
            # Internal id when this mapping is used.

            Field('uri', {'mini': 0, 'maxi': 1},
                  primitives.URIField, None),
            # Identifies what this mapping refers to.

            Field('name', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Names what this mapping refers to.

            Field('comments', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None)
            # Versions, Issues, Scope limitations etc..
        ])
        return elm


StructureDefinitionMappingField = StructureDefinitionMapping()


class StructureDefinitionDifferential(ComplexElement):
    """ Differential view of the structure.

    A differential view is expressed relative to the base StructureDefinition -
    a statement of differences that it applies.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('element', {'mini': 1, 'maxi': -1},
                  ElementDefinitionField(), None)
            # Definition of elements in the resource
            # (if no StructureDefinition).
        ])
        return elm


StructureDefinitionDifferentialField = StructureDefinitionDifferential()


class StructureDefinitionSnapshot(ComplexElement):
    """ Snapshot view of the structure.

    A snapshot view is expressed in a stand alone form that can be used and
    interpreted without considering the base StructureDefinition.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('element', {'mini': 1, 'maxi': 1},
                  ElementDefinitionField(), None)
            # Definition of elements in the resource
            # (if no StructureDefinition).
        ])
        return elm


StructureDefinitionSnapshotField = StructureDefinitionSnapshot()


class StructureDefinition(DomainResource):
    """ Structural Definition.

    A definition of a FHIR structure. This resource is used to describe the
    underlying resources, data types defined in FHIR, and also for describing
    extensions, and constraints on resources and data types.
    """

    url = Column(primitives.URIField, nullable=False)
    # Absolute URL used to reference this StructureDefinition.

    version = Column(primitives.StringField)
    # Logical id for this version of the StructureDefinition.

    name = Column(primitives.StringField, nullable=False)
    # Informal name for this StructureDefinition.

    display = Column(primitives.StringField)
    # Use this name when displaying the value.

    status = Column(primitives.CodeField, nullable=False)
    # draft | active | retired.

    experimental = Column(primitives.BooleanField)
    # If for testing purposes, not real usage.

    publisher = Column(primitives.StringField)
    # Name of the publisher (Organization or individual).

    date = Column(primitives.DateTimeField)
    # Date for this version of the StructureDefinition.

    description = Column(primitives.StringField)
    # Natural language description of the StructureDefinition.

    requirements = Column(primitives.StringField)
    # Scope and Usage this structure definition is for.

    copyright = Column(primitives.StringField)
    # Use and/or publishing restrictions.

    fhirVersion = Column(primitives.IdField)
    # FHIR Version this StructureDefinition targets.

    kind = Column(primitives.CodeField, nullable=False)
    # datatype | resource | logical.

    constrainedType = Column(primitives.CodeField)
    # Any datatype or resource, including abstract ones.

    abstract = Column(primitives.BooleanField, nullable=False)
    # Whether the structure is abstract.

    context = Column(Array(primitives.StringField))
    # Where the extension can be used in instances.

    contextType = Column(primitives.CodeField)
    # resource | datatype | mapping | extension.

    base = Column(primitives.URIField)
    # Structure that this set of constraints applies to.

    identifier = Column(Array(complex.IdentifierField()))
    # Other identifiers for the StructureDefinition.

    useContext = Column(Array(complex.CodeableConceptField()))
    # Content intends to support these contexts.

    code = Column(Array(complex.CodingField()))
    # Assist with indexing and finding.

    contact = Column(Array(StructureDefinitionContactField()))
    # Contact details of the publisher.

    mapping = Column(Array(StructureDefinitionMappingField()))
    # External specification that the content is mapped to.

    differential = Column(StructureDefinitionDifferentialField())
    # Differential view of the structure.

    snapshot = Column(StructureDefinitionSnapshotField())
    # Snapshot view of the structure.

    def _resource_summary(self):
        summary_fields = ['id', 'meta', 'identifier', 'description', ]
        return {
            'repr': '%r' % self.description,
            'fields': summary_fields
        }
