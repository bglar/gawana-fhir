#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/SampledData)
#  Date: 2016-03-18.


from sqlalchemy import Column
from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field
from fhir_server.elements.complex.quantity import SimpleQuantityField


class SampledData(ComplexElement):
    """ A series of measurements taken by a device.

    A series of measurements taken by a device, with upper and lower limits.
    There may be more than one dimension in the data.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('data', {'mini': 1, 'maxi': 1},
                  primitives.StringField, None),
            # Decimal values with spaces, or "E" | "U" | "L".

            Field('dimensions', {'mini': 1, 'maxi': 1},
                  primitives.PositiveIntField, None),
            # Number of sample points at each time point.

            Field('factor', {'mini': 0, 'maxi': 1},
                  primitives.DecimalField, None),
            # Multiply data by this before adding to origin.

            Field('lowerLimit', {'mini': 0, 'maxi': 1},
                  primitives.DecimalField, None),
            # Lower limit of detection.

            Field('period', {'mini': 1, 'maxi': 1},
                  primitives.DecimalField, None),
            # Number of milliseconds between samples.

            Field('upperLimit', {'mini': 0, 'maxi': 1},
                  primitives.DecimalField, None),
            # Upper limit of detection.

            Field('origin', {'mini': 1, 'maxi': 1},
                  SimpleQuantityField(), None),
            # zero values and units
        ])
        return elm


SampledDataField = SampledData()
