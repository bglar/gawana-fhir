from fhir_server.resources.base.resource_profile_manager import (
    ResourceProfile,
    XMLProfileManager,
)

constraints1 = {
    "resource": "Organization",
    "fields": [
        {"name": "active", "cardinality": {"mini": 0, "maxi": 1}},
        {"name": "name", "cardinality": {"mini": 0, "maxi": 1}},
    ],
}

org_profile1 = ResourceProfile(constraints1)
DemoOrgResource1 = org_profile1.apply_constraints()

# The following profiled resource uses constraints from an xml file.

profile_file_path = "fhir_server/profiles/gawana-default.structuredefinition.xml"
cls_instance = XMLProfileManager(profile_file_path)
constraints = cls_instance.construct_constraints()

org_profile = ResourceProfile(constraints)
DemoOrgResource = org_profile.apply_constraints()
