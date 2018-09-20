#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Money)
#  Date: 2016-03-18.

from sqlalchemy import Column
from fhir_server.elements import primitives
from .quantity import Quantity, Field


class Money(Quantity):
    """ An amount of money. With regard to precision, see [Decimal
    Precision](datatypes.html#precision).

    There SHALL be a code if there is a value and it SHALL be an
    expression of currency.  If system is present, it SHALL be
    ISO 4217 (system = "urn:iso:std:iso:4217" - currency).
    """
    def __init__(self, *args, **kwargs):
        self.fields = [
            Column('extension', primitives.StringField),
            # Additional Content defined by implementations.

            Column('id', primitives.StringField)
            # xml:id (or equivalent in JSON).
        ]
        self.precision = 19
        self.scale = 4

        if 'precision' in kwargs:
            self.precision = kwargs['precision']
        if 'scale' in kwargs:
            self.scale = kwargs['scale']

    def element_properties(self):
        elements = super().element_properties()

        # Get the value field from quantity and give it a default precision
        # and scale of (19, 4)
        for count, elm in enumerate(elements):
            if elm.name == 'value':
                elements.pop(count)

                field = Field(
                    'value', {'mini': 0, 'maxi': 1},
                    primitives.DecimalField(self.precision, self.scale), None)
                elements.append(field)

        return elements


MoneyField = Money()
