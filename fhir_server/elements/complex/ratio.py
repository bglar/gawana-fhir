#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Ratio)
#  Date: 2016-03-18.

from fhir_server.elements.base.complex_element import ComplexElement, Field
from fhir_server.elements.complex.quantity import QuantityField


class Ratio(ComplexElement):
    """ A ratio of two Quantity values - a numerator and a denominator.

    A relationship of two Quantity values - expressed as a numerator and a
    denominator.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("denominator", {"mini": 0, "maxi": 1}, QuantityField(), None),
                # Denominator value.
                Field("numerator", {"mini": 0, "maxi": 1}, QuantityField(), None)
                # Numerator value.
            ]
        )
        return elm


RatioField = Ratio()
