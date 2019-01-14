#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/HumanName)
#  Date: 2016-03-18.

from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field
from fhir_server.elements.complex.period import PeriodField


class HumanName(ComplexElement):
    """ Name of a human - parts and usage.

    A human's name with the ability to identify parts and usage.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("family", {"mini": 0, "maxi": -1}, primitives.StringField, None),
                # Family name (often called 'Surname').
                Field("given", {"mini": 0, "maxi": -1}, primitives.StringField, None),
                # Given names (not always 'first'). Includes middle names.
                Field("prefix", {"mini": 0, "maxi": -1}, primitives.StringField, None),
                # Parts that come before the name.
                Field("suffix", {"mini": 0, "maxi": -1}, primitives.StringField, None),
                # Parts that come after the name.
                Field("text", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # Text representation of the full name.
                Field("use", {"mini": 0, "maxi": 1}, primitives.CodeField, None),
                # usual | official | temp | nickname | anonymous | old | maiden.
                Field("period", {"mini": 0, "maxi": 1}, PeriodField(), None)
                # Time period when name was/is in use.
            ]
        )
        return elm


HumanNameField = HumanName()
