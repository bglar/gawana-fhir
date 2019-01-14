#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/ContactPoint)
#  Date: 2016-03-18.


from sqlalchemy import Column, ForeignKey
from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field
from fhir_server.elements.complex.period import PeriodField


class ContactPoint(ComplexElement):
    """ Details of a Technology mediated contact point (phone, fax, email, etc.).

    Details for all kinds of technology mediated contact points for a
    person or organization, including telephone, email, etc.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field(
                    "rank", {"mini": 0, "maxi": 1}, primitives.PositiveIntField, None
                ),
                # Specify preferred order of use (1 = highest).
                Field("system", {"mini": 0, "maxi": 1}, primitives.CodeField, None),
                # phone | fax | email | pager | other.
                Field("use", {"mini": 0, "maxi": 1}, primitives.CodeField, None),
                # home | work | temp | old | mobile-purpose of this contact point.
                Field("value", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # The actual contact point details.
                Field("period", {"mini": 0, "maxi": 1}, PeriodField(), None)
                # Time period when the contact point was/is in use.
            ]
        )
        return elm


ContactPointField = ContactPoint()
