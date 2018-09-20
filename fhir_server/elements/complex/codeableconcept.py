#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/CodeableConcept)
#  Date: 2016-03-18.

from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field
from fhir_server.elements.complex.coding import CodingField


class CodeableConcept(ComplexElement):
    """ Concept - reference to a terminology or just  text.

    A concept that may be defined by a formal reference to a
    terminology or ontology or may be provided by text.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('text', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Plain text representation of the concept.

            Field('coding', {'mini': 0, 'maxi': -1}, CodingField(), None),
            # Code defined by a terminology system.
        ])
        return elm


CodeableConceptField = CodeableConcept()
