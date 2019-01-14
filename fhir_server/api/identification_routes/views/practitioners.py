from fhir_server.resources import Practitioner
from fhir_server.api.mixins import (
    ListMixin,
    CreateMixin,
    UpdateMixin,
    RetrieveMixin,
    DestroyMixin,
)


class PractitionerListView(ListMixin, CreateMixin):
    """List or Create Practitioner instances."""

    resource = Practitioner


class PractitionerDetailView(UpdateMixin, RetrieveMixin, DestroyMixin):
    """Retrieve, update or delete Practitioner instances."""

    resource = Practitioner


practitioner_list = PractitionerListView.as_view("practitioner_list")
practitioner_detail = PractitionerDetailView.as_view("practitioner_detail")
