#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Identifier)
#  Date: 2016-03-18.


from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field
from fhir_server.elements.complex.period import PeriodField
from fhir_server.elements.complex.codeableconcept import CodeableConceptField
from fhir_server.elements.complex.reference import ReferenceField


class Identifier(ComplexElement):
    """ An identifier intended for computation.

    A technical identifier - identifies some entity uniquely and unambiguously.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("system", {"mini": 0, "maxi": 1}, primitives.URIField, None),
                # The namespace for the identifier.
                Field("use", {"mini": 0, "maxi": 1}, primitives.CodeField, None),
                # usual | official | temp | secondary (If known).
                Field("value", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # The value that is unique.
                Field(
                    "assigner",
                    {"mini": 0, "maxi": 1},
                    ReferenceField(),
                    ["Organization"],
                ),
                # Organization that issued id (may be just text).
                Field("period", {"mini": 0, "maxi": 1}, PeriodField(), None),
                # Time period when id is/was valid for use.
                Field("type", {"mini": 0, "maxi": 1}, CodeableConceptField(), None),
                # Description of identifier.
            ]
        )
        return elm


IdentifierField = Identifier()
