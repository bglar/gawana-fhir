from sqlalchemy import Column
from sqlalchemy_utils import CompositeArray as Array

from fhir_server.elements import primitives, Field, complex
from fhir_server.elements.base.backboneelement import BackboneElement
from fhir_server.resources.domainresource import DomainResource


class BundleEntryRequest(BackboneElement):
    """ Transaction Related Information.

    Additional information about how this entry should be processed as part of
    a transaction.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("method", {"mini": 1, "maxi": 1}, primitives.CodeField, None),
                # GET | POST | PUT | DELETE.
                Field("url", {"mini": 1, "maxi": 1}, primitives.URIField, None),
                # URL for HTTP equivalent of this entry.
                Field(
                    "ifNoneMatch", {"mini": 0, "maxi": 1}, primitives.StringField, None
                ),
                # For managing cache currency.
                Field(
                    "ifModifiedSince",
                    {"mini": 0, "maxi": 1},
                    primitives.InstantField,
                    None,
                ),
                # For managing update contention.
                Field("ifMatch", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # For managing update contention.
                Field(
                    "ifNoneExist", {"mini": 0, "maxi": 1}, primitives.StringField, None
                ),
                # For conditional creates.
            ]
        )
        return elm


BundleEntryRequestField = BundleEntryRequest()


class BundleEntryResponse(BackboneElement):
    """ Transaction Related Information.

    Additional information about how this entry should be processed as part of
    a transaction.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("etag", {"mini": 0, "maxi": 1}, primitives.StringField, None),
                # The etag for the resource (if relevant).
                Field(
                    "lastModified",
                    {"mini": 0, "maxi": 1},
                    primitives.InstantField,
                    None,
                ),
                # Server's date time modified.
                Field("location", {"mini": 0, "maxi": 1}, primitives.URIField, None),
                # """ The location, if the operation returns a location.
                Field("status", {"mini": 1, "maxi": 1}, primitives.CodeField, None),
                # Status return code for entry.
                Field(
                    "outcome",
                    {"mini": 1, "maxi": 1},
                    complex.ReferenceField(),
                    ["OperationOutcome"],
                ),
            ]
        )
        return elm


BundleEntryResponseField = BundleEntryResponse()


class BundleEntrySearch(BackboneElement):
    """ Search related information.

    Information about the search process that lead to the creation of this
    entry.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("mode", {"mini": 0, "maxi": 1}, primitives.CodeField, None),
                # match | include | outcome - why this is in the result set.
                Field("score", {"mini": 0, "maxi": 1}, primitives.DecimalField, None)
                # Search ranking (between 0 and 1).
            ]
        )
        return elm


BundleEntrySearchField = BundleEntrySearch()


class BundleLink(BackboneElement):
    """ Links related to this Bundle.

    A series of links that provide context to this bundle.
    """

    resource_name = "BundleLink"

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("relation", {"mini": 1, "maxi": 1}, primitives.StringField, None),
                # http://www.iana.org/assignments/link-relations/link-relations.xhtml.
                Field("url", {"mini": 1, "maxi": 1}, primitives.URIField, None)
                # Reference details for the link.
            ]
        )
        return elm


BundleLinkField = BundleLink()


class BundleEntry(BackboneElement):
    """ Entry in the bundle - will have a resource, or information.

    An entry in a bundle resource - will either contain a resource, or
    information about a resource (transactions and history only).
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("fullUrl", {"mini": 0, "maxi": 1}, primitives.URIField, None),
                # Absolute URL for resource (server address, or UUID/OID).
                Field("link", {"mini": 0, "maxi": -1}, BundleLinkField(), None),
                # Links related to this entry.
                Field(
                    "request", {"mini": 0, "maxi": 1}, BundleEntryRequestField(), None
                ),
                # Transaction Related Information.
                Field(
                    "response", {"mini": 0, "maxi": 1}, BundleEntryResponseField(), None
                ),
                # Transaction Related Information.
                Field("search", {"mini": 0, "maxi": 1}, BundleEntrySearchField(), None),
                # Search related information.
                Field(
                    "resource", {"mini": 0, "maxi": 1}, complex.ReferenceField(), "all"
                ),
                # A resource in the bundle.
                # TODO is this the best approach for this field?
                # It is a Resource field in the spec, but here we save the
                # reference and use reference resolution when accessing a Bundle.
            ]
        )
        return elm


BundleEntryField = BundleEntry()


class Bundle(DomainResource):
    """ Contains a collection of resources.

    A container for a collection of resources.
    """

    type = Column(primitives.CodeField, nullable=False)
    # document | message | transaction | transaction-response |
    # batch | batch-response | history | searchset | collection

    total = Column(primitives.UnsignedIntField)
    # If search, the total number of matches

    link = Column(Array(BundleLinkField()))
    # Links related to this Bundle

    signature = Column(complex.SignatureField())
    # Digital Signature

    entry = Column(Array(BundleEntryField()))
    # Entry in the bundle - will have a resource, or information must be
    # a resource unless there's a request or response. The fullUrl element
    # must be present when a resource is present, and not present otherwise

    def _resource_summary(self):
        summary_fields = ["id", "meta", "type", "total"]
        return {
            "repr": "type: %r, link: %r" % (self.type, self.type),
            "fields": summary_fields,
        }

    def __repr__(self):
        return "<Bundle %r>" % self.id
