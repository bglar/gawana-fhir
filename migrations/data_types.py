from fhir_server.resources.structuredefinition import (
    StructureDefinitionContactField, StructureDefinitionSnapshotField,
    StructureDefinitionMappingField, StructureDefinitionDifferentialField)

from fhir_server.elements.complex import *
from fhir_server.elements.elementdefinition import *
from fhir_server.elements.meta import *
from fhir_server.resources.conformance.valueset import *
from fhir_server.resources.domainresource import *
from fhir_server.resources.identification.healthcareservice import (
    HealthcareServiceAvailableTimeField, HealthcareServiceNotAvailableField)
from fhir_server.resources.identification.location import LocationPositionField
from fhir_server.resources.identification.organization import (
    OrganizationContactField)
from fhir_server.resources.identification.patient import (
    PatientLinkField, PatientContactField,
    PatientCommunicationField)
from fhir_server.resources.identification.practitioner import (
    PractitionerPractitionerRoleField, PractitionerQualificationField)

Fields = {
    # Meta field common to all resources
    'meta': MetaField,

    # complex elements
    'address': AddressField,
    'age': AgeField,
    'annotation': AnnotationField,
    'attachment': AttachmentField,
    'codeableconcept': CodeableConceptField,
    'coding': CodingField,
    'contactpoint': ContactPointField,
    'count': CountField,
    'distance': DistanceField,
    'duration': DurationField,
    'humanname': HumanNameField,
    'identifier': IdentifierField,
    'money': MoneyField,
    'period': PeriodField,
    'quantity': QuantityField,
    'range': RangeField,
    'ratio': RatioField,
    'sampleddata': SampledDataField,
    'signature': SignatureField,
    'timing': TimingField,
    'narrative': NarrativeField,
    'reference': ReferenceField,

    # backbone elements for all the resources
    'organizationcontact': OrganizationContactField,

    # Extension element
    'extension': ElementExtension,

    # Element definition element
    'elementdefinition': ElementDefinitionField,

    # Structure definition Fields
    'structuredefinitioncontact': StructureDefinitionContactField,
    'structuredefinitionsnapshot': StructureDefinitionSnapshotField,
    'structuredefinitionmapping': StructureDefinitionMappingField,
    'structuredefinitiondifferential': StructureDefinitionDifferentialField,

    # valueset resource backbone elemtnts
    'valuesetcodesystemconceptdesignation':
        ValueSetCodeSystemConceptDesignationField,
    'valuesetcodesystemconcept': ValueSetCodeSystemConceptField,
    'valuesetcodesystem': ValueSetCodeSystemField,
    'valuesetcomposeincludeconcept': ValueSetComposeIncludeConceptField,
    'valuesetcomposeincludefilter': ValueSetComposeIncludeFilterField,
    'valuesetcomposeinclude': ValueSetComposeIncludeField,
    'valuesetcompose': ValueSetComposeField,
    'valuesetcontact': ValueSetContactField,
    'valuesetexpansioncontains': ValueSetExpansionContainsField,
    'valuesetexpansionparameter': ValueSetExpansionParameterField,
    'valuesetexpansion': ValueSetExpansionField,

    # location resource backbone elements
    'locationposition': LocationPositionField,

    # healthcareservice backbone elements
    'healthcareserviceavailabletime': HealthcareServiceAvailableTimeField,
    'healthcareservicenotavailable': HealthcareServiceNotAvailableField,

    # practitioner backbone elements
    'practitionerpractitionerrole': PractitionerPractitionerRoleField,
    'practitionerqualification': PractitionerQualificationField,

    # patientlink backbone elements
    'patientanimal': PatientLinkField,
    'patientcommunication': PatientCommunicationField,
    'patientcontact': PatientContactField,
    'patientlink': PatientLinkField
}
