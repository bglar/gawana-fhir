#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Reference)
#  Date: 2016-03-22.


from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field


class Reference(ComplexElement):
    """ A reference from one resource to another.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('display', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Text alternative for the resource.

            Field('reference', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None)
            # Relative, internal or absolute URL reference.
        ])
        return elm


ReferenceField = Reference()
