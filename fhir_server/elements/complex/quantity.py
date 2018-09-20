#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Quantity)
#  Date: 2016-03-18.

from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field


class SimpleQuantity(ComplexElement):
    """ A fixed quantity (no comparator). """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('code', {'mini': 0, 'maxi': 1},
                  primitives.CodeField, None),
            # Coded form of the unit.

            Field('system', {'mini': 0, 'maxi': 1},
                  primitives.URIField, None),
            # System that defines coded unit form.

            Field('unit', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Unit representation.

            Field('value', {'mini': 0, 'maxi': 1},
                  primitives.DecimalField, None)
            # Numerical value (with implicit precision).
        ])
        return elm


class Quantity(SimpleQuantity):
    """ A measured or measurable amount.

    A measured amount (or an amount that can potentially be measured). Note
    that measured amounts include amounts that are not precisely quantified,
    including amounts involving arbitrary units and floating currencies.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('comparator', {'mini': 0, 'maxi': 1},
                  primitives.CodeField, None)
            # < | <= | >= | > - how to understand the value.
        ])
        return elm


SimpleQuantityField = SimpleQuantity()
QuantityField = Quantity()
