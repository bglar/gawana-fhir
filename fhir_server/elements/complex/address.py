#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Address)
#  Date: 2016-03-18.

from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field
from fhir_server.elements.complex.period import PeriodField


class Address(ComplexElement):
    """ A postal address.

    There is a variety of postal address formats defined around the
    world. This format defines a superset that is the basis for all
    addresses around the world.
    """
    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('city', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Name of city, town etc..

            Field('country', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Country (can be ISO 3166 3 letter code).

            Field('district', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # District name (aka county)

            Field('line', {'mini': 0, 'maxi': -1},
                  primitives.StringField, None),
            # Street name, number, direction & P.O. Box etc..

            Field('postalCode', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Postal code for area.

            Field('state', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Sub-unit of country (abbreviations ok).

            Field('type', {'mini': 0, 'maxi': 1},
                  primitives.CodeField, None),
            # postal | physical | both.

            Field('text', {'mini': 0, 'maxi': 1}, primitives.StringField, None),
            # Text representation of the address.

            Field('use', {'mini': 0, 'maxi': 1}, primitives.CodeField, None),
            # home | work | temp | old - purpose of this address.

            Field('period', {'mini': 0, 'maxi': 1}, PeriodField(), None)
            # Time period when address was/is in use.
        ])
        return elm


AddressField = Address()
