#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Narrative)
#  Date: 2016-03-22.


from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field


class Narrative(ComplexElement):
    """ A human-readable formatted text, including images.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("div", {"mini": 1, "maxi": 1}, primitives.StringField, None),
                # Limited xhtml content.
                # TODO xhtml field
                Field("status", {"mini": 1, "maxi": 1}, primitives.CodeField, None)
                # generated | extensions | additional | empty.
            ]
        )
        return elm


NarrativeField = Narrative()
