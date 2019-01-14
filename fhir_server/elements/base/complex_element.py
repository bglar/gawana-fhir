from collections import namedtuple
import abc

from sqlalchemy import Column
from sqlalchemy_utils import CompositeArray

from fhir_server.elements import primitives
from fhir_server.elements.extension import ElementExtension
from .complex_mixin import PgComposite


Field = namedtuple("Field", ["name", "cardinality", "type", "reference"])


class ComplexElement(object):
    """ Base for all complex elements.

    Base definition for all complex elements in a resource.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        self.fields = [
            Column("id", primitives.StringField),
            # xml:id (or equivalent in JSON).
            Column("extension", CompositeArray(ElementExtension()))
            # Additional Content defined by implementations.
        ]

    def __call__(self, *args, **kwargs):
        return self.generate_element_definition()

    @abc.abstractmethod
    def element_properties(self):
        """Create and return an array with the fields for the child element"""
        return []

    def generate_element_definition(self):
        properties = self.element_properties()

        if len(properties) > 0:
            for prop in properties:
                name = prop.name
                nullable = True if (prop.cardinality["mini"] == 0) else False

                field_type = (
                    CompositeArray(prop.type)
                    if (prop.cardinality["maxi"] == -1)
                    else prop.type
                )

                new_column = Column(name, field_type, nullable=nullable)

                field_names = [col.name for col in self.fields]
                if name not in field_names:
                    self.fields.append(new_column)

        data_type = "fhir_%s" % self.__class__.__name__.lower()
        return PgComposite(data_type, self.fields)
