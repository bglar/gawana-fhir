#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Signature)
#  Date: 2016-03-18.

from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field
from fhir_server.elements.complex.coding import CodingField
from fhir_server.elements.complex.reference import ReferenceField


class Signature(ComplexElement):
    """ A digital Signature - XML DigSig, JWT, Graphical image of signature, etc..

    A digital signature along with supporting context. The signature may be
    electronic/cryptographic in nature, or a graphical image representing a
    hand-written signature, or a signature process. Different Signature
    approaches have different data_types.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('blob', {'mini': 1, 'maxi': 1},
                  primitives.Base64Field, None),
            # The actual signature content (XML DigSig. JWT, picture, etc.).

            Field('contentType', {'mini': 1, 'maxi': 1},
                  primitives.CodeField, None),
            # The technical format of the signature.

            Field('when', {'mini': 1, 'maxi': 1},
                  primitives.InstantField, None),
            # When the signature was created.

            Field('whoUri', {'mini': 1, 'maxi': 1},
                  primitives.URIField, None),
            # Who signed the signature.

            Field('whoReference', {'mini': 1, 'maxi': 1}, ReferenceField(),
                  ['Practitioner', 'RelatedPerson', 'Patient', 'Device',
                  'Organization']),
            # Who signed the signature.

            Field('type', {'mini': 1, 'maxi': -1},
                  CodingField(), None)
            # Indication of the reason the entity signed the object(s).
        ])
        return elm


SignatureField = Signature()
