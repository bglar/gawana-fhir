#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Period)
#  Date: 2016-03-18.

from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field


class Period(ComplexElement):
    """ Time range defined by start and end date/time.

    A time period defined by a start and end date and optionally time.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('end', {'mini': 0, 'maxi': 1},
                  primitives.DateTimeField, None),
            # End time with inclusive boundary, if not ongoing.

            Field('start', {'mini': 0, 'maxi': 1},
                  primitives.DateTimeField, None)
            # Starting time with inclusive boundary.
        ])
        return elm


PeriodField = Period()
