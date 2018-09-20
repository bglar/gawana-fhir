#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Meta)
#  Date: 2016-03-22.

from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field
from fhir_server.elements.complex.coding import CodingField


class Meta(ComplexElement):
    """ Metadata about a resource.

    The metadata about a resource. This is content in the resource that is
    maintained by the infrastructure. Changes to the content may not always be
    associated with version changes to the resource.
    """
    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('versionId', {'mini': 0, 'maxi': 1},
                  primitives.IdField, None),
            # Version specific identifier.

            Field('lastUpdated', {'mini': 0, 'maxi': 1},
                  primitives.InstantField, None),
            # When the resource version last changed.

            Field('profile', {'mini': 0, 'maxi': -1},
                  primitives.URIField, None),
            # Profiles this resource claims to conform to.

            Field('security', {'mini': 0, 'maxi': -1},
                  CodingField(), None),
            # Security Labels applied to this resource.

            Field('tag', {'mini': 0, 'maxi': -1}, CodingField(), None)
            # Tags applied to this resource.
        ])
        return elm


MetaField = Meta()
