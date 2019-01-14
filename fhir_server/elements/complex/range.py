#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Range)
#  Date: 2016-03-18.


from fhir_server.elements.base.complex_element import ComplexElement, Field
from fhir_server.elements.complex.quantity import SimpleQuantityField


class Range(ComplexElement):
    """ Set of values bounded by low and high.

    A set of ordered Quantities defined by a low and high limit.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("high", {"mini": 0, "maxi": 1}, SimpleQuantityField(), None),
                # High limit.
                Field("low", {"mini": 0, "maxi": 1}, SimpleQuantityField(), None)
                # Low limit.
            ]
        )
        return elm


RangeField = Range()
