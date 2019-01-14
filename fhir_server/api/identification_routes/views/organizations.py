from fhir_server.resources import Organization
from fhir_server.api.mixins import (
    ListMixin,
    CreateMixin,
    UpdateMixin,
    RetrieveMixin,
    DestroyMixin,
)


class OrganizationListView(ListMixin, CreateMixin, UpdateMixin, DestroyMixin):
    """List or Create Organization instances."""

    resource = Organization


class OrganizationDetailView(UpdateMixin, RetrieveMixin, DestroyMixin):
    """Retrieve, update or delete organization instances."""

    resource = Organization


organization_list = OrganizationListView.as_view("organization_list")
organization_detail = OrganizationDetailView.as_view("organization_detail")
