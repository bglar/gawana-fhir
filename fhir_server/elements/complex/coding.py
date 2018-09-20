#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Coding)
#  Date: 2016-03-18.

from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field


class Coding(ComplexElement):
    """ A reference to a code defined by a terminology system. """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('code', {'mini': 0, 'maxi': 1},
                  primitives.CodeField, None),
            # Symbol in syntax defined by the system.

            Field('display', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Representation defined by the system.

            Field('system', {'mini': 0, 'maxi': 1},
                  primitives.URIField, None),
            # Identity of the terminology system.

            Field('userSelected', {'mini': 0, 'maxi': 1},
                  primitives.BooleanField, None),
            # If this coding was chosen directly by the user.

            Field('version', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Version of the system - if relevant.
        ])
        return elm


CodingField = Coding()
