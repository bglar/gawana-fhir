from fhir_server.resources import HealthcareService
from fhir_server.api.mixins import (
    ListMixin,
    CreateMixin,
    UpdateMixin,
    RetrieveMixin,
    DestroyMixin,
)


class HealthcareServiceListView(ListMixin, CreateMixin):
    """List or Create HealthCareService instances."""

    resource = HealthcareService


class HealthcareServiceDetailView(UpdateMixin, RetrieveMixin, DestroyMixin):
    """Retrieve, update or delete HealthCareService instances."""

    resource = HealthcareService


healthcareservice_list = HealthcareServiceListView.as_view("healthcareservice_list")
healthcareservice_detail = HealthcareServiceDetailView.as_view(
    "healthcareservice_detail"
)
