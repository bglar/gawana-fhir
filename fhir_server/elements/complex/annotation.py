#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Annotation)
#  Date: 2016-03-18.

from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field
from fhir_server.elements.complex.reference import ReferenceField


class Annotation(ComplexElement):
    """ Text node with attribution.

    A  text note which also  contains information about who made the
    statement and when.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field(
                    "authorString", {"mini": 0, "maxi": 1}, primitives.StringField, None
                ),
                # Individual responsible for the annotation.
                Field("text", {"mini": 1, "maxi": 1}, primitives.StringField, None),
                # The annotation  - text content.
                Field("time", {"mini": 0, "maxi": 1}, primitives.DateTimeField, None),
                # When the annotation was made.
                Field(
                    "authorReference",
                    {"mini": 0, "maxi": 1},
                    ReferenceField(),
                    ["Practitioner", "Patient", "RelatedPerson"],
                ),
                # Individual responsible for the annotation.
            ]
        )
        return elm


AnnotationField = Annotation()
