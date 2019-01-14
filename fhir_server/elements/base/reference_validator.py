import re
import requests

from fhir_server.configs import INTERNAL_SERVER_URL

url_regex = (
    "((http|https):\/\/([A-Za-z0-9\\\/\.\-\:\%\$])*)?(Account|"
    "AllergyIntolerance|Endpoint|"
    "Appointment|AppointmentResponse|AuditEvent|Basic|Binary|BodySite|Bundle|"
    "CarePlan|Claim|ClaimResponse|ClinicalImpression|Communication|"
    "CommunicationRequest|Composition|ConceptMap|Condition|Conformance|"
    "Contract|Coverage|DataElement|DetectedIssue|Device|DeviceComponent|"
    "DeviceMetric|DeviceUseRequest|DeviceUseStatement|DiagnosticOrder|"
    "DiagnosticReport|DocumentManifest|DocumentReference|EligibilityRequest|"
    "EligibilityResponse|Encounter|EnrollmentRequest|EnrollmentResponse|"
    "EpisodeOfCare|ExplanationOfBenefit|FamilyMemberHistory|Flag|Goal|Group|"
    "HealthcareService|ImagingObjectSelection|ImagingStudy|Immunization|"
    "ImmunizationRecommendation|ImplementationGuide|List|Location|Media|"
    "Medication|MedicationAdministration|MedicationDispense|MedicationOrder|"
    "MedicationStatement|MessageHeader|NamingSystem|NutritionOrder|"
    "Observation|OperationDefinition|OperationOutcome|Order|OrderResponse|"
    "Organization|Patient|PaymentNotice|PaymentReconciliation|Person|"
    "Practitioner|Procedure|ProcedureRequest|ProcessRequest|ProcessResponse|"
    "Provenance|Questionnaire|QuestionnaireResponse|ReferralRequest|"
    "RelatedPerson|RiskAssessment|Schedule|SearchParameter|Slot|Specimen|"
    "StructureDefinition|Subscription|Substance|SupplyDelivery|SupplyRequest|"
    "TestScript|ValueSet|VisionPrescription)\/[A-Za-z0-9\-\.]{1,64}"
    "(\/_history\/[A-Za-z0-9\-\.]{1,64})?"
)


def reference_resolution(url):
    data = requests.get(url)
    if data.status_code != 200:
        raise TypeError("We were unable to resolve a resource reference at %s" % url)


def validate_reference(ref_str):
    pattern = re.compile(url_regex)
    if pattern.fullmatch(ref_str):
        if ref_str.startswith("http"):
            reference_resolution(ref_str)

        else:
            # url = INTERNAL_SERVER_URL + ref_str
            # reference_resolution(url)
            pass

    else:
        raise TypeError(
            "The reference provided is not valid. Please provide a valid url"
        )
