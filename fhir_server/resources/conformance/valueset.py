from sqlalchemy import Column
from sqlalchemy_utils import CompositeArray as Array

from fhir_server.elements import (
    ComplexElement, Field, primitives, complex)
from fhir_server.resources.domainresource import DomainResource


class ValueSetCodeSystemConceptDesignation(ComplexElement):
    """ Additional representations for the concept.

    Additional representations for the concept - other languages, aliases,
    specialized purposes, used for particular purposes, etc.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('language', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Human language of the designation.

            Field('value', {'mini': 1, 'maxi': 1},
                  primitives.StringField, None),
            # The text value for this designation.

            Field('use', {'mini': 0, 'maxi': 1},
                  complex.CodingField(), None)
            # Details how this designation would be used.
        ])
        return elm


ValueSetCodeSystemConceptDesignationField = \
    ValueSetCodeSystemConceptDesignation()


class ValueSetCodeSystemConcept(ComplexElement):
    """ Concepts in the code system.

    Concepts that are in the code system. The concept definitions are
    inherently hierarchical, but the definitions must be consulted to determine
    what the meaning of the hierarchical relationships are.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('code', {'mini': 1, 'maxi': 1},
                  primitives.CodeField, None),
            # Code that identifies concept.

            Field('abstract', {'mini': 0, 'maxi': 1},
                  primitives.BooleanField, None),
            # If this code is not for use as a real concept.

            Field('display', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Text to display to the user.

            Field('definition', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Formal definition.

            Field('concept', {'mini': 0, 'maxi': -1},
                  primitives.StringField, 'Self'),
            # Child Concepts (is-a/contains/categorizes).
            # TODO Reference resolution mechanism for backbone elements

            Field('designation', {'mini': 0, 'maxi': 1},
                  ValueSetCodeSystemConceptDesignationField(), None),
            # Additional representation for the concept
        ])
        return elm


ValueSetCodeSystemConceptField = ValueSetCodeSystemConcept()


class ValueSetCodeSystem(ComplexElement):
    """ An inline code system, which is part of this value set.

    A definition of a code system, inlined into the value set (as a packaging
    convenience). Note that the inline code system may be used from other value
    sets by referring to its (codeSystem.system) directly.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('system', {'mini': 1, 'maxi': 1},
                  primitives.URIField, None),
            # URI to identify the code system (e.g. in Coding.system).

            Field('version', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Version (for use in Coding.version).

            Field('caseSensitive', {'mini': 0, 'maxi': 1},
                  primitives.BooleanField, None),
            # If code comparison is case sensitive.

            Field('concept', {'mini': 0, 'maxi': -1},
                  ValueSetCodeSystemConceptField(), None),
            # Concepts in the code system.
        ])
        return elm


ValueSetCodeSystemField = ValueSetCodeSystem()


class ValueSetComposeIncludeConcept(ComplexElement):
    """ A concept defined in the system.

    Specifies a concept to be included or excluded.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('code', {'mini': 1, 'maxi': 1},
                  primitives.StringField, None),
            # Code or expression from system.

            Field('display', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Test to display for this code for this value set.

            Field('designation', {'mini': 0, 'maxi': -1},
                  ValueSetCodeSystemConceptDesignationField(), None)
            # Additional representations for this valueset.
        ])
        return elm


ValueSetComposeIncludeConceptField = ValueSetComposeIncludeConcept()


class ValueSetComposeIncludeFilter(ComplexElement):
    """ Select codes/concepts by their properties (including relationships).

    Select concepts by specify a matching criteria based on the properties
    (including relationships) defined by the system. If multiple filters are
    specified, they SHALL all be true.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('op', {'mini': 1, 'maxi': 1},
                  primitives.CodeField, None),
            # = | is-a | is-not-a | regex | in | not-in.

            Field('property', {'mini': 1, 'maxi': 1},
                  primitives.CodeField, None),
            # A property defined by the code system.

            Field('value', {'mini': 1, 'maxi': 1},
                  primitives.CodeField, None)
            # Code from the system, or regex criteria.
        ])
        return elm


ValueSetComposeIncludeFilterField = ValueSetComposeIncludeFilter()


class ValueSetComposeInclude(ComplexElement):
    """ Include one or more codes from a code system.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('system', {'mini': 1, 'maxi': 1},
                  primitives.CodeField, None),
            # The system the codes come from.

            Field('version', {'mini': 0, 'maxi': 1},
                  primitives.CodeField, None),
            # Specific version of the code system referred to.

            Field('concept', {'mini': 0, 'maxi': -1},
                  ValueSetComposeIncludeConceptField(), None),
            # A concept defined in the system.

            Field('filter', {'mini': 0, 'maxi': -1},
                  ValueSetComposeIncludeFilterField(), None),
            # Select codes/concepts by their properties
            # (including relationships).JSON).
        ])
        return elm


ValueSetComposeIncludeField = ValueSetComposeInclude()


class ValueSetCompose(ComplexElement):
    """ When value set includes codes from elsewhere.

    A set of criteria that provide the content logical definition of the value
    set by including or excluding codes from outside this value set.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('compose_import', {'mini': 0, 'maxi': -1},
                  primitives.URIField, None),
            # Import the contents of another value set.

            Field('include', {'mini': 0, 'maxi': -1},
                  ValueSetComposeIncludeField(), None),
            # Include one or more codes from a code system.

            Field('exclude', {'mini': 0, 'maxi': -1},
                  ValueSetComposeIncludeField(), None)
            # Explicitly exclude codes.
        ])
        return elm


ValueSetComposeField = ValueSetCompose()


class ValueSetContact(ComplexElement):
    """ Contact details of the publisher.

    Contacts to assist a user in finding and communicating with the publisher.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('name', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Name of an individual to contact.

            Field('telecom', {'mini': 0, 'maxi': -1},
                  complex.ContactPointField(), None)
            # Contact details for individual or publisher.
        ])
        return elm


ValueSetContactField = ValueSetContact()


class ValueSetExpansionContains(ComplexElement):
    """ Codes in the value set.

    The codes that are contained in the value set expansion.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('abstract', {'mini': 0, 'maxi': 1},
                  primitives.BooleanField, None),
            # If user cannot select this entry.

            Field('code', {'mini': 0, 'maxi': 1},
                  primitives.CodeField, None),
            # Code - if blank, this is not a selectable code.

            Field('display', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # User display for the concept.

            Field('system', {'mini': 0, 'maxi': 1},
                  primitives.URIField, None),
            # System value for the code.

            Field('version', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Version in which this code/display is defined.

            Field('contains', {'mini': 0, 'maxi': -1},
                  primitives.StringField, 'Self')
            # des contained under this entry.
            # TODO Reference resolution mechanism for backbone elements
        ])
        return elm


ValueSetExpansionContainsField = ValueSetExpansionContains()


class ValueSetExpansionParameter(ComplexElement):
    """ Parameter that controlled the expansion process.

    A parameter that controlled the expansion process. These parameters may be
    used by users of expanded value sets to check whether the expansion is
    suitable for a particular purpose, or to pick the correct expansion.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('name', {'mini': 1, 'maxi': 1},
                  primitives.StringField, None),
            # Name as assigned by the server.

            Field('valueBoolean', {'mini': 0, 'maxi': 1},
                  primitives.BooleanField, None),
            # Value of the named parameter.

            Field('valueCode', {'mini': 0, 'maxi': 1},
                  primitives.CodeField, None),
            # Value of the named parameter.

            Field('valueDecimal', {'mini': 0, 'maxi': 1},
                  primitives.DecimalField, None),
            # Value of the named parameter.

            Field('valueInteger', {'mini': 0, 'maxi': 1},
                  primitives.IntegerField, None),
            # Value of the named parameter.

            Field('valueString', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Value of the named parameter.

            Field('valueUri', {'mini': 0, 'maxi': 1},
                  primitives.URIField, None),
            # Value of the named parameter.
        ])
        return elm


ValueSetExpansionParameterField = ValueSetExpansionParameter()


class ValueSetExpansion(ComplexElement):
    """ Used when the value set is "expanded".

    A value set can also be "expanded", where the value set is turned into a
    simple collection of enumerated codes. This element holds the expansion, if
    it has been performed.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('identifier', {'mini': 1, 'maxi': 1},
                  primitives.URIField, None),
            # Uniquely identifies this expansion.

            Field('timestamp', {'mini': 1, 'maxi': 1},
                  primitives.DateTimeField, None),
            # Time ValueSet expansion happened.

            Field('offset', {'mini': 0, 'maxi': 1},
                  primitives.IntegerField, None),
            # Offset at which this resource starts.

            Field('total', {'mini': 0, 'maxi': 1},
                  primitives.IntegerField, None),
            # Total number of codes in the expansion.

            Field('parameter', {'mini': 0, 'maxi': 1},
                  ValueSetExpansionParameterField(), None),
            # Parameter that controlled the expansion process.

            Field('contains', {'mini': 0, 'maxi': 1},
                  ValueSetExpansionContainsField(), None),
            # Codes in the value set.
        ])
        return elm


ValueSetExpansionField = ValueSetExpansion()


class ValueSet(DomainResource):
    """ A set of codes drawn from one or more code systems.

    A value set specifies a set of codes drawn from one or more code systems.
    """

    url = Column(primitives.URIField)
    # Globally unique logical identifier for  value set.

    version = Column(primitives.StringField)
    # Logical identifier for this version of the value set.

    name = Column(primitives.StringField)
    # Informal name for this value set.

    status = Column(primitives.CodeField, nullable=False)
    # draft | active | retired.

    experimental = Column(primitives.BooleanField)
    # If for testing purposes, not real usage.

    publisher = Column(primitives.StringField)
    # Name of the publisher (organization or individual).

    date = Column(primitives.DateTimeField)
    # Date for given status.

    lockedDate = Column(primitives.DateField)
    # Fixed date for all referenced code systems and value sets.

    description = Column(primitives.StringField)
    # Human language description of the value set.

    immutable = Column(primitives.BooleanField)
    # Indicates whether or not any change to the content logical
    # definition may occur.

    requirements = Column(primitives.StringField)
    # Why needed.

    copyright = Column(primitives.StringField)
    # Use and/or publishing restrictions.

    extensible = Column(primitives.BooleanField)
    # Whether this is intended to be used with an extensible binding.

    identifier = Column(complex.IdentifierField())
    #  Additional identifier for the value set (e.g. HL7 v2 / CDA)

    contact = Column(Array(ValueSetContactField()))
    # Contact details of the publisher.

    useContext = Column(Array(complex.CodeableConceptField()))
    # Content intends to support these contexts.

    codeSystem = Column(ValueSetCodeSystemField())
    # An inline code system, which is part of this value set.

    compose = Column(ValueSetComposeField())
    # When value set includes codes from elsewhere.

    expansion = Column(ValueSetExpansionField())
    # Used when the value set is "expanded".

    def _resource_summary(self):
        summary_fields = ['id', 'meta', 'identifier', 'description', ]
        return {
            'repr': '%r' % self.description,
            'fields': summary_fields
        }
