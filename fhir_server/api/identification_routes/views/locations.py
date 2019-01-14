from fhir_server.resources import Location
from fhir_server.api.mixins import (
    ListMixin,
    CreateMixin,
    UpdateMixin,
    RetrieveMixin,
    DestroyMixin,
)


class LocationListView(ListMixin, CreateMixin):
    """List or Create Location instances."""

    resource = Location


class LocationDetailView(UpdateMixin, RetrieveMixin, DestroyMixin):
    """Retrieve, update or delete Location instances."""

    resource = Location


location_list = LocationListView.as_view("location_list")
location_detail = LocationDetailView.as_view("location_detail")
