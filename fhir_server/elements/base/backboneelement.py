import abc

from fhir_server.elements.extension import ElementExtension
from .complex_element import ComplexElement, Field


class BackboneElement(ComplexElement):
    """ Base for elements defined inside a resource.

    Base definition for all elements that are defined inside a resource - but
    not those in a data type.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('modifierExtension', {'mini': 0, 'maxi': -1},
                  ElementExtension(), None)
            # Extensions that cannot be ignored.
        ])
        return elm
