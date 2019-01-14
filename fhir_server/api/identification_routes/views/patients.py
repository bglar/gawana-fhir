from fhir_server.resources import Patient
from fhir_server.api.mixins import (
    ListMixin,
    CreateMixin,
    UpdateMixin,
    RetrieveMixin,
    DestroyMixin,
)


class PatientListView(ListMixin, CreateMixin):
    """List or Create Patient instances."""

    resource = Patient


class PatientDetailView(UpdateMixin, RetrieveMixin, DestroyMixin):
    """Retrieve, update or delete Patient instances."""

    resource = Patient


patient_list = PatientListView.as_view("patient_list")
patient_detail = PatientDetailView.as_view("patient_detail")
