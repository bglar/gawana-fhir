from abc import ABCMeta, abstractmethod

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import JSONType
from sqlalchemy_utils import CompositeArray as Array

from fhir_server.elements import complex
from fhir_server.resources.resource import Resource
from fhir_server.elements.extension import ElementExtension


class DomainResource(Resource):
    """ A resource with narrative, extensions, and contained resources.

    A resource that includes narrative, extensions, and contained resources.
    """

    __abstract__ = True
    __metaclass__ = ABCMeta

    @declared_attr
    def text(cls):
        # Text summary of the resource, for human interpretation
        return Column(complex.NarrativeField())

    @declared_attr
    def contained(cls):
        # Contained, inline Resources
        return Column(Array(JSONType))

    @declared_attr
    def extension(cls):
        # Additional Content defined by implementations
        return Column(Array(ElementExtension()))

    @declared_attr
    def modifierExtension(cls):
        # Extensions that cannot be ignored
        return Column(Array(ElementExtension()))

    @abstractmethod
    def _resource_summary(self):
        """Resource summary.

        All resource instances should define a summary fields and a logical
        text field that can be used to subset the resource.

        expected implementation::
            ```
            def _resource_summary(self):
                summary_fields = ['field1', 'field2']
                return {
                    'repr': '%r' % self.field1,
                    'fields': summary_fields
                }
            ```
        :return:
        """
        raise NotImplementedError("Resources should implement a summary!")

    @abstractmethod
    def __repr__(cls):
        raise NotImplementedError("Resources should implement a `repr` method!")
