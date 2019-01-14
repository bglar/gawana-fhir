from sqlalchemy import Column
from sqlalchemy_utils import CompositeArray as Array
from fhir_server.elements import primitives, complex, Field, OpenType
from fhir_server.elements.base.backboneelement import BackboneElement
from fhir_server.resources.domainresource import DomainResource


class QuestionnaireItemOption(BackboneElement):
    """Only allow data when.

    enableWhen must contain either an 'answer' or an 'answered' element
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("value", {"mini": 1, "maxi": 1}, OpenType(), None)
                # Question that determines whether item is enabled
            ]
        )
        return elm


QuestionnaireItemOptionField = QuestionnaireItemOption()


class QuestionnaireItemEnableWhen(BackboneElement):
    """Only allow data when.

    enableWhen must contain either an 'answer' or an 'answered' element
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("question", {"mini": 1, "maxi": 1}, primitives.StringField, None),
                # Question that determines whether item is enabled
                Field(
                    "answered", {"mini": 0, "maxi": 1}, primitives.BooleanField, None
                ),
                # Enable when answered or not
                Field("answer", {"mini": 0, "maxi": 1}, OpenType(), None)
                # Value question must have
            ]
        )
        return elm


QuestionnaireItemEnableWhenField = QuestionnaireItemEnableWhen()


class QuestionnaireItem(BackboneElement):
    """Questions and sections within the Questionnaire.

    Maximum length can only be declared for simple question types
    Group items must have nested items, display items cannot have nested items
    Display items cannot have a "concept" asserted
    Only 'choice' items can have options
    A question cannot have both option and options
    Required and repeat aren't permitted for display items
    Read-only can't be specified for "display" items
    Default values can't be specified for groups or display items
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("linkId", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # To link questionnaire with questionnaire response
                Field("concept", {"mini": 0, "maxi": -1}, complex.CodingField(), None),
                # Concept that represents this item within in a questionnaire
                Field("prefix", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # E.g. "1(a)", "2.5.3"
                Field("text", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # Primary text for the item
                Field("type", {"mini": 1, "maxi": 1}, primitives.StringField, None),
                # group | display | boolean | decimal | integer | date | dateTime
                Field("required", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # Whether the item must be included in data results
                Field("repeats", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # Whether the item may repeat
                Field("readOnly", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # Don't allow human editing
                Field(
                    "maxLength", {"mini": 0, "maxi": 1}, primitives.IntegerField, None
                ),
                # No more than this many characters
                Field(
                    "options",
                    {"mini": 0, "maxi": 1},
                    complex.ReferenceField(),
                    ["ValueSet"],
                ),
                # Valueset containing permitted answers
                Field(
                    "enableWhen",
                    {"mini": 0, "maxi": -1},
                    QuestionnaireItemEnableWhenField(),
                    None,
                ),
                # Value question must have
                Field(
                    "option",
                    {"mini": 0, "maxi": -1},
                    QuestionnaireItemOptionField(),
                    None,
                ),
                # Permitted answer
                Field("initial", {"mini": 0, "maxi": 1}, OpenType(), None),
                # Initial presumed answer for question
                Field(
                    "item", {"mini": 0, "maxi": -1}, complex.ReferenceField, ["Self"]
                ),
                # Permitted answers
            ]
        )
        return elm


QuestionnaireItemField = QuestionnaireItem()


class Questionnaire(DomainResource):
    """ A structured set of questions.

    A structured set of questions intended to guide the collection of answers.
    The questions are ordered and grouped into coherent subsets, corresponding
    to the structure of the grouping of the underlying questions.
    """

    url = Column(primitives.URIField)
    # Globally unique logical identifier for questionnaire

    version = Column(primitives.StringField)
    # Logical identifier for this version of Questionnaire

    status = Column(primitives.CodeField, nullable=False)
    # draft | published | retired

    date = Column(primitives.DateTimeField)
    # Date this version was authored

    publisher = Column(primitives.StringField)
    # Organization/individual who designed the questionnaire

    title = Column(primitives.StringField)
    # Name for the questionnaire

    subjectType = Column(Array(primitives.CodeField))
    # Resource that can be subject of QuestionnaireResponse

    identifier = Column(Array(complex.IdentifierField()))
    # External identifiers for this questionnaire

    telecom = Column(Array(complex.ContactPointField()))
    # Contact information of the publisher

    useContext = Column(Array(complex.CodeableConceptField))
    # Questionnaire intends to support these contexts

    concept = Column(Array(complex.CodingField))
    # Concept that represents the overall questionnaire

    item = Column(Array(QuestionnaireItemField()))

    def _resource_summary(self):
        summary_fields = ["id", "meta", "type", "total"]
        return {
            "repr": "type: %r, link: %r" % (self.type, self.type),
            "fields": summary_fields,
        }

    def __repr__(self):
        return "<OperationOutcome %r>" % self.id
