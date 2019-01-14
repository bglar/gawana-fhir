from fhir_server.elements import primitives, complex, ComplexElement, Field
from fhir_server.elements.opentype import OpenType


class ElementDefinitionBase(ComplexElement):
    """ Base definition information for tools.

    Information about the base definition of the element, provided to make it
    unnecessary for tools to trace the deviation of the element through the
    derived and related profiles. This information is only provided where the
    element definition represents a constraint on another element definition,
    and must be present if there is a base element definition.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("max", {"mini": 1, "maxi": 1}, primitives.StringField, None),
                # Max cardinality of the base element.
                Field("min", {"mini": 1, "maxi": 1}, primitives.IntegerField, None),
                # Min cardinality of the base element.
                Field("path", {"mini": 1, "maxi": 1}, primitives.StringField, None),
                # Path that identifies the base element.
            ]
        )
        return elm


ElementDefinitionBaseField = ElementDefinitionBase()


class ElementDefinitionBinding(ComplexElement):
    """ ValueSet details if this is coded.

    Binds to a value set if this element is coded (code, Coding,
    CodeableConcept).
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field(
                    "description", {"mini": 0, "maxi": 1}, primitives.StringField, None
                ),
                # Human explanation of the value set.
                Field("strength", {"mini": 1, "maxi": 1}, primitives.CodeField, None),
                # required | extensible | preferred | example.
                Field(
                    "valueSetReference",
                    {"mini": 0, "maxi": 1},
                    complex.ReferenceField(),
                    "Valuesets",
                ),
                # Source of value set.
                Field("valueSetUri", {"mini": 0, "maxi": 1}, primitives.URIField, None),
                # Source of value set.
            ]
        )
        return elm


ElementDefinitionBindingField = ElementDefinitionBinding()


class ElementDefinitionConstraint(ComplexElement):
    """ Condition that must evaluate to true.

    Formal constraints such as co-occurrence and other constraints that can be
    computationally evaluated within the context of the instance.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("human", {"mini": 1, "maxi": 1}, primitives.StringField, None),
                # Human description of constraint.
                Field("key", {"mini": 1, "maxi": 1}, primitives.IdField, None),
                # Target of 'condition' reference above.
                Field(
                    "requirements", {"mini": 0, "maxi": 1}, primitives.StringField, None
                ),
                # Why this constraint necessary or appropriate.
                Field("severity", {"mini": 1, "maxi": 1}, primitives.CodeField, None),
                # error | warning.
                Field("xpath", {"mini": 1, "maxi": 1}, primitives.StringField, None),
                # XPath expression of constraint.
            ]
        )
        return elm


ElementDefinitionConstraintField = ElementDefinitionConstraint()


class ElementDefinitionMapping(ComplexElement):
    """ Map element to another set of definitions.

    Identifies a concept from an external specification that roughly
    corresponds to this element.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("identity", {"mini": 1, "maxi": 1}, primitives.IdField, None),
                # Reference to mapping declaration.
                Field("language", {"mini": 0, "maxi": 1}, primitives.CodeField, None),
                # Computable language of mapping.
                Field("map", {"mini": 1, "maxi": 1}, primitives.StringField, None),
                # Details of the mapping.
            ]
        )
        return elm


ElementDefinitionMappingField = ElementDefinitionMapping()


class ElementDefinitionSlicing(ComplexElement):
    """ This element is sliced - slices follow.

    Indicates that the element is sliced into a set of alternative definitions
    (i.e. in a structure definition, there are multiple different constraints
    on a single element in the base resource). Slicing can be used in any
    resource that has cardinality ..* on the base resource, or any resource
    with a choice of types. The set of slices is any elements that come after
    this in the element sequence that have the same path, until a shorter path
    occurs (the shorter path terminates the set).
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field(
                    "description", {"mini": 0, "maxi": 1}, primitives.StringField, None
                ),
                # Text description of how slicing works (or not).
                Field(
                    "discriminator",
                    {"mini": 0, "maxi": -1},
                    primitives.StringField,
                    None,
                ),
                # Element values that used to distinguish the slices.
                Field("ordered", {"mini": 0, "maxi": 1}, primitives.BooleanField, None),
                # If elements must be in same order as slices.
                Field("rules", {"mini": 1, "maxi": 1}, primitives.CodeField, None),
                # closed | open | openAtEnd.
            ]
        )
        return elm


ElementDefinitionSlicingField = ElementDefinitionSlicing()


class ElementDefinitionType(ComplexElement):
    """ Data type and Profile for this element.

    The data type or resource that the value of this element is permitted to
    be.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field(
                    "aggregation", {"mini": 0, "maxi": -1}, primitives.CodeField, None
                ),
                # contained | referenced | bundled - how aggregated.
                Field("code", {"mini": 1, "maxi": 1}, primitives.StringField, None),
                # Name of Data type or Resource.
                Field("profile", {"mini": 0, "maxi": -1}, primitives.URIField, None),
                # Profile (StructureDefinition) to apply (or IG).
            ]
        )
        return elm


ElementDefinitionTypeField = ElementDefinitionType()


class ElementDefinition(ComplexElement):
    """ Definition of an element in a resource or extension.

    Captures constraints on each element within the resource, profile, or
    extension.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("path", {"mini": 1, "maxi": 1}, primitives.StringField, None),
                # The path of the element (see the Detailed Descriptions).
                Field(
                    "representation",
                    {"mini": 0, "maxi": -1},
                    primitives.CodeField,
                    None,
                ),
                # How this element is represented in instances.
                Field("name", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # Name for this particular element definition (reference target).
                Field("label", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # Name for element to display with or prompt for element.
                Field("short", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # Concise definition for xml presentation.
                Field(
                    "definition", {"mini": 0, "maxi": 1}, primitives.MarkdownField, None
                ),
                # Full formal definition as narrative text.
                Field(
                    "comments", {"mini": 0, "maxi": 1}, primitives.MarkdownField, None
                ),
                # Comments about the use of this element.
                Field(
                    "requirements",
                    {"mini": 0, "maxi": 1},
                    primitives.MarkdownField,
                    None,
                ),
                # Why is this needed?.
                Field("alias", {"mini": 0, "maxi": -1}, primitives.StringField, None),
                # Other names.
                Field("min", {"mini": 0, "maxi": 1}, primitives.IntegerField, None),
                # Minimum Cardinality.
                Field("max", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # Maximum Cardinality (a number or *).
                Field(
                    "nameReference",
                    {"mini": 0, "maxi": 1},
                    primitives.StringField,
                    None,
                ),
                # To another element constraint (by element.name).
                Field(
                    "meaningWhenMissing",
                    {"mini": 0, "maxi": 1},
                    primitives.MarkdownField,
                    None,
                ),
                # Implicit meaning when this element is missing
                Field(
                    "maxLength", {"mini": 0, "maxi": 1}, primitives.IntegerField, None
                ),
                # Max length of strings
                Field("condition", {"mini": 0, "maxi": -1}, primitives.IdField, None),
                # Reference to invariant about presence.
                Field(
                    "mustSupport", {"mini": 0, "maxi": 1}, primitives.BooleanField, None
                ),
                # If the element must supported
                Field(
                    "isModifier", {"mini": 0, "maxi": 1}, primitives.BooleanField, None
                ),
                # If this modifies the meaning of other elements.
                Field(
                    "isSummary", {"mini": 0, "maxi": 1}, primitives.BooleanField, None
                ),
                # Include when _summary = true?.
                Field("defaultValue", {"mini": 0, "maxi": 1}, OpenType, None),
                # Specified value it missing from instance
                Field("fixed", {"mini": 0, "maxi": 1}, OpenType, None),
                # Value must be exactly this
                Field("pattern", {"mini": 0, "maxi": 1}, OpenType, None),
                # Value must have at least these property values
                Field("example", {"mini": 0, "maxi": 1}, OpenType, None),
                # Example value: [as defined for type]
                Field("minValue", {"mini": 0, "maxi": 1}, OpenType, None),
                # Minimum Allowed Value (for some types)
                Field("maxValue", {"mini": 0, "maxi": 1}, OpenType, None),
                # Maximum Allowed Value (for some types)
                Field("code", {"mini": 0, "maxi": -1}, complex.CodingField(), None),
                # Defining code.
                Field(
                    "slicing",
                    {"mini": 0, "maxi": 1},
                    ElementDefinitionSlicingField(),
                    None,
                ),
                # This element is sliced - slices follow.
                Field(
                    "base", {"mini": 0, "maxi": 1}, ElementDefinitionBaseField(), None
                ),
                # Base definition information for tools.
                Field(
                    "type", {"mini": 0, "maxi": -1}, ElementDefinitionTypeField(), None
                ),
                # Data type and Profile for this element.
                Field(
                    "constraint",
                    {"mini": 0, "maxi": -1},
                    ElementDefinitionConstraintField(),
                    None,
                ),
                # Condition that must evaluate to true.
                Field(
                    "binding",
                    {"mini": 0, "maxi": 1},
                    ElementDefinitionBindingField(),
                    None,
                ),
                # ValueSet details if this is coded.
                Field(
                    "mapping",
                    {"mini": 0, "maxi": -1},
                    ElementDefinitionMappingField(),
                    None,
                ),
                # Map element to another set of definitions.
            ]
        )
        return elm


ElementDefinitionField = ElementDefinition()
