#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Attachment)
#  Date: 2016-03-18.


from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field


class Attachment(ComplexElement):
    """Content in a format defined elsewhere.

    For referring to data content defined in other formats.
    """
    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('contentType', {'mini': 0, 'maxi': 1},
                  primitives.CodeField, None),
            # Mime type of the content, with charset etc.self.

            Field('creation', {'mini': 0, 'maxi': 1},
                  primitives.DateTimeField, None),
            # Date attachment was first created.

            Field('data', {'mini': 0, 'maxi': 1},
                  primitives.Base64Field, None),
            # Data inline, base64ed.

            Field('language', {'mini': 0, 'maxi': 1},
                  primitives.CodeField, None),
            # Human language of the content (BCP-47).

            Field('hash', {'mini': 0, 'maxi': 1},
                  primitives.Base64Field, None),
            # Hash of the data (sha-1, base64ed).

            Field('size', {'mini': 0, 'maxi': 1},
                  primitives.UnsignedIntField, None),
            # Number of bytes of content (if url provided).

            Field('title', {'mini': 0, 'maxi': 1},
                  primitives.StringField, None),
            # Label to display in place of the data.

            Field('url', {'mini': 0, 'maxi': 1},
                  primitives.URIField, None)
            # Uri where the data can be found.
        ])
        return elm


AttachmentField = Attachment()
