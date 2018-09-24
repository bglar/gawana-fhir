# PAGINATION PARAMS
ITEMS_PER_PAGE = 10

VALID_XML_MIMETYPES = [
    'xml',
    'text/xml',
    'application/xml',
    'application/xml+fhir'
]

VALID_JSON_MIMETYPES = [
    'json',
    'application/json',
    'application/json+fhir'
]

# Add configs for swappable valueset urls
# VALUESETS_BASE_URL = 'http://my-server-url/valuesets/'
VALUESETS_BASE_URL = 'http://127.0.0.1:5000/'
ADDRESS_USE_URL = VALUESETS_BASE_URL + 'address_use/'
ADDRESS_TYPE_URL = VALUESETS_BASE_URL + 'address_type/'
QUANTITY_COMPARATOR_URL = VALUESETS_BASE_URL + 'quantity_comparator/'
HUMANNAME_USE_URL = VALUESETS_BASE_URL + 'name_use/'
UNITS_OF_TIME_URL = VALUESETS_BASE_URL + 'units_of_time/'
EVENT_TIMING_URL = VALUESETS_BASE_URL + 'event_timing/'
TIMING_ABBREVIATION_URL = VALUESETS_BASE_URL + 'timing_abbreviation/'
CONTACT_POINT_SYSTEM_URL = VALUESETS_BASE_URL + 'contact_point_system/'
CONTACT_POINT_USE_URL = VALUESETS_BASE_URL + 'contact_point_use/'
SIGNATURE_TYPE_URL = VALUESETS_BASE_URL + 'signature_type/'
IDENTIFIER_TYPE_URL = VALUESETS_BASE_URL + 'identifier_type/'
IDENTIFIER_USE_URL = VALUESETS_BASE_URL + 'identifier_use/'
AGE_UNITS_URL = VALUESETS_BASE_URL + 'age_unit/'
NARRATIVE_STATUS_URL = VALUESETS_BASE_URL + 'narrative_status/'
CONTACT_ENTITY_TYPE_URL = VALUESETS_BASE_URL + 'contactentity_type/'
ORGANIZATION_TYPE_URL = VALUESETS_BASE_URL + 'organization_type/'

LOCATION_STATUS_URL = VALUESETS_BASE_URL + 'location_status/'
LOCATION_MODE_URL = VALUESETS_BASE_URL + 'location_mode/'
SERVICE_DELIVERY_LOCATION_ROLE_TYPE_URL = (
    VALUESETS_BASE_URL + 'RoleCode/')
LOCATION_PHYSICAL_TYPE_URI = VALUESETS_BASE_URL + 'location_physical_type/'

SERVICE_CATEGORY_URL = VALUESETS_BASE_URL + 'service_category/'
SERVICE_TYPE_URL = VALUESETS_BASE_URL + 'service_type/'
C80_PRACTICE_CODES_URL = VALUESETS_BASE_URL + 'c80_practice_codes/'
SERVICE_PROVISION_CONDITIONS_URL = (
    VALUESETS_BASE_URL + 'service_provision_conditions/')
REFERRAL_METHOD_URL = VALUESETS_BASE_URL + 'service_referral_method/'
DAYS_OF_WEEK = VALUESETS_BASE_URL + 'days_of_week/'

ADMINISTRATIVE_GENDER_URL = VALUESETS_BASE_URL + 'administrative_gender/'
PRACTITIONER_ROLE_URL = VALUESETS_BASE_URL + 'practitioner_role/'
PRACTITIONER_SPECIALITY_URL = VALUESETS_BASE_URL + 'practitioner_specialty/'
ANZSCO_OCCUPATIONS_URL = VALUESETS_BASE_URL + 'anzsco_occupations/'
LANGUAGE_URI = VALUESETS_BASE_URL + 'language/'

MARITAL_STATUS_URL = VALUESETS_BASE_URL + 'marital_status/'
PATIENT_CONTACT_RELATIONSHIP_URL = (
    VALUESETS_BASE_URL + 'patient_contact_relationship/')
ANIMAL_SPECIES_URL = VALUESETS_BASE_URL + 'animal_species/'
ANIMAL_BREEDS_URL = VALUESETS_BASE_URL + 'animal_breeds/'
GENDER_STATUS_URL = VALUESETS_BASE_URL + 'animal_genderstatus/'
LINK_TYPE_URL = VALUESETS_BASE_URL + 'link_type/'

ISSUE_SEVERITY_URL = VALUESETS_BASE_URL + 'issue_severity/'
ISSUE_TYPE_URL = VALUESETS_BASE_URL + 'issue_type/'
OPERATION_OUTCOME_URL = VALUESETS_BASE_URL + 'operation_outcome/'

UCUM_SYSTEM_URI = 'http://unitsofmeasure.org'

VALID_ATTACHMENT_EXTENSIONS = [
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
    '.pdf',
    '.txt',
    '.doc',
    '.docx',
    'image/jpeg'
]

SIGNATURE_MIME_TYPES = [
    'application/jwt',
    'image/jpeg'
]

INTERNAL_SERVER_URL = 'http://localhost:5000/api/v1/'

SANCTIONED_CODE_URLS = [
    'http://ihtsdo.org',
    'http://www.nlm.nih.gov/',
    'http://loinc.org',
    'http://unitsofmeasure.org',
    'http://ncimeta.nci.nih.gov',
    'http://www.ama-assn.org/go/cpt',
    'http://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/NDFRT/',
    'http://www.fda.gov/Drugs/InformationOnDrugs/ucm142438.htm',
    'http://www.fda.gov/Drugs/InformationOnDrugs/ucm142438.htm',
    'http://www2a.cdc.gov/vaccines/iis/iisstandards/vaccines.asp?rpt=cvx',
    'http://www.iso.org/iso/country_codes.htm',
    'http://www.nubc.org',
    'http://www.radlex.org',
    'http://www.who.int/classifications/icd/en/',
    'http://www.icd10data.com/icd10pcs',
    'http://www.cms.gov/Medicare/Coding/ICD10/',
    'http://www.cdc.gov/nchs/icd/icd9.htm',
    'http://www.ph3c.org/',
    'http://www.who.int/classifications/icf/en/',
    'https://www.hl7.org/implement/standards/product_brief.cfm?product_id=186',
    'http://www.whocc.no/atc/structure_and_principles/',
    'http://tools.ietf.org/html/bcp47',
    'http://tools.ietf.org/html/bcp13',
    'http://hit-testing.nist.gov:13110/rtmms/index.html#rosetta',
    'http://hl7.org/fhir/surface.html',
    'http://hl7.org/fhir/account-status.html',
    'http://hl7.org/fhir/actionlist.html',
    'http://hl7.org/fhir/additionalmaterials.html',
    'http://hl7.org/fhir/address-type.html',
    'http://hl7.org/fhir/address-use.html',
    'http://hl7.org/fhir/adjudication.html',
    'http://hl7.org/fhir/adjudication-error.html',
    'http://hl7.org/fhir/adjustment-reason.html',
    'http://hl7.org/fhir/administrative-gender.html',
    'http://hl7.org/fhir/encounter-admit-source.html',
    'http://hl7.org/fhir/allergy-intolerance-category.html',
    'http://hl7.org/fhir/allergy-intolerance-criticality.html',
    'http://hl7.org/fhir/allergy-intolerance-status.html',
    'http://hl7.org/fhir/allergy-intolerance-type.html',
    'http://hl7.org/fhir/animal-breeds.html',
    'http://hl7.org/fhir/animal-genderstatus.html',
    'http://hl7.org/fhir/animal-species.html',
    'http://hl7.org/fhir/answer-format.html',
    'http://hl7.org/fhir/appointmentstatus.html',
    'http://hl7.org/fhir/assert-direction-codes.html',
    'http://hl7.org/fhir/assert-operator-codes.html',
    'http://hl7.org/fhir/assert-response-code-types.html',
    'http://hl7.org/fhir/audit-event-action.html',
    'http://hl7.org/fhir/audit-event-outcome.html',
    'http://hl7.org/fhir/audit-event-type.html',
    'http://hl7.org/fhir/basic-resource-type.html',
    'http://hl7.org/fhir/binding-strength.html',
    'http://hl7.org/fhir/bundle-type.html',
    'http://hl7.org/fhir/care-plan-activity-category.html',
    'http://hl7.org/fhir/care-plan-activity-status.html',
    'http://hl7.org/fhir/care-plan-relationship.html',
    'http://hl7.org/fhir/care-plan-status.html',
    'http://hl7.org/fhir/choice-list-orientation.html',
    'http://hl7.org/fhir/claim-type-link.html',
    'http://hl7.org/fhir/claim-use-link.html',
    'http://hl7.org/fhir/classification-or-context.html',
    'http://hl7.org/fhir/clinical-impression-status.html',
    'http://hl7.org/fhir/communication-request-status.html',
    'http://hl7.org/fhir/communication-status.html',
    'http://hl7.org/fhir/composition-attestation-mode.html',
    'http://hl7.org/fhir/composition-status.html',
    'http://hl7.org/fhir/concept-map-equivalence.html',
    'http://hl7.org/fhir/condition-category.html',
    'http://hl7.org/fhir/condition-clinical.html',
    'http://hl7.org/fhir/condition-state.html',
    'http://hl7.org/fhir/condition-ver-status.html',
    'http://hl7.org/fhir/conditional-delete-status.html',
    'http://hl7.org/fhir/conformance-expectation.html',
    'http://hl7.org/fhir/conformance-resource-status.html',
    'http://hl7.org/fhir/conformance-statement-kind.html',
    'http://hl7.org/fhir/constraint-severity.html',
    'http://hl7.org/fhir/contact-point-system.html',
    'http://hl7.org/fhir/contact-point-use.html',
    'http://hl7.org/fhir/contactentity-type.html',
    'http://hl7.org/fhir/content-type.html',
    'http://hl7.org/fhir/contract-signer-type.html',
    'http://hl7.org/fhir/contract-subtype.html',
    'http://hl7.org/fhir/contract-term-subtype.html',
    'http://hl7.org/fhir/contract-term-type.html',
    'http://hl7.org/fhir/contract-type.html',
    'http://hl7.org/fhir/data-absent-reason.html',
    'http://hl7.org/fhir/data-types.html',
    'http://hl7.org/fhir/dataelement-stringency.html',
    'http://hl7.org/fhir/days-of-week.html',
    'http://hl7.org/fhir/detectedissue-severity.html',
    'http://hl7.org/fhir/device-action.html',
    'http://hl7.org/fhir/device-use-request-priority.html',
    'http://hl7.org/fhir/device-use-request-status.html',
    'http://hl7.org/fhir/devicestatus.html',
    'http://hl7.org/fhir/diagnostic-order-priority.html',
    'http://hl7.org/fhir/diagnostic-order-status.html',
    'http://hl7.org/fhir/diagnostic-report-status.html',
    'http://hl7.org/fhir/encounter-diet.html',
    'http://hl7.org/fhir/digital-media-type.html',
    'http://hl7.org/fhir/encounter-discharge-disposition.html',
    'http://hl7.org/fhir/document-mode.html',
    'http://hl7.org/fhir/document-reference-status.html',
    'http://hl7.org/fhir/document-relationship-type.html',
    'http://hl7.org/fhir/encounter-class.html',
    'http://hl7.org/fhir/encounter-location-status.html',
    'http://hl7.org/fhir/encounter-priority.html',
    'http://hl7.org/fhir/encounter-special-arrangements.html',
    'http://hl7.org/fhir/encounter-state.html',
    'http://hl7.org/fhir/encounter-type.html',
    'http://hl7.org/fhir/entformula-additive.html',
    'http://hl7.org/fhir/episode-of-care-status.html',
    'http://hl7.org/fhir/service-uscls.html',
    'http://hl7.org/fhir/teeth.html',
    'http://hl7.org/fhir/oral-prosthodontic-material.html',
    'http://hl7.org/fhir/service-pharmacy.html',
    'http://hl7.org/fhir/service-product.html',
    'http://hl7.org/fhir/tooth.html',
    'http://hl7.org/fhir/udi.html',
    'http://hl7.org/fhir/vision-product.html',
    'http://hl7.org/fhir/claim-exception.html',
    'http://hl7.org/fhir/extension-context.html',
    'http://hl7.org/fhir/filter-operator.html',
    'http://hl7.org/fhir/flag-category.html',
    'http://hl7.org/fhir/flag-priority.html',
    'http://hl7.org/fhir/flag-status.html',
    'http://hl7.org/fhir/fm-conditions.html',
    'http://hl7.org/fhir/forms.html',
    'http://hl7.org/fhir/fundsreserve.html',
    'http://hl7.org/fhir/goal-acceptance-status.html',
    'http://hl7.org/fhir/goal-category.html',
    'http://hl7.org/fhir/goal-priority.html',
    'http://hl7.org/fhir/goal-relationship-type.html',
    'http://hl7.org/fhir/goal-status.html',
    'http://hl7.org/fhir/goal-status-reason.html',
    'http://hl7.org/fhir/group-type.html',
    'http://hl7.org/fhir/guide-dependency-type.html',
    'http://hl7.org/fhir/guide-page-kind.html',
    'http://hl7.org/fhir/guide-resource-purpose.html',
    'http://hl7.org/fhir/history-status.html',
    'http://hl7.org/fhir/http-verb.html',
    'http://hl7.org/fhir/identifier-type.html',
    'http://hl7.org/fhir/identifier-use.html',
    'http://hl7.org/fhir/identity-assuranceLevel.html',
    'http://hl7.org/fhir/immunization-recommendation-date-criterion.html',
    'http://hl7.org/fhir/immunization-recommendation-status.html',
    'http://hl7.org/fhir/intervention.html',
    'http://hl7.org/fhir/issue-severity.html',
    'http://hl7.org/fhir/issue-type.html',
    'http://hl7.org/fhir/link-type.html',
    'http://hl7.org/fhir/list-empty-reason.html',
    'http://hl7.org/fhir/list-example-codes.html',
    'http://hl7.org/fhir/list-mode.html',
    'http://hl7.org/fhir/list-order.html',
    'http://hl7.org/fhir/list-status.html',
    'http://hl7.org/fhir/location-mode.html',
    'http://hl7.org/fhir/location-physical-type.html',
    'http://hl7.org/fhir/location-status.html',
    'http://hl7.org/fhir/marital-status.html',
    'http://hl7.org/fhir/measurement-principle.html',
    'http://hl7.org/fhir/digital-media-subtype.html',
    'http://hl7.org/fhir/medication-admin-status.html',
    'http://hl7.org/fhir/medication-dispense-status.html',
    'http://hl7.org/fhir/medication-order-status.html',
    'http://hl7.org/fhir/medication-statement-status.html',
    'http://hl7.org/fhir/message-conformance-event-mode.html',
    'http://hl7.org/fhir/message-events.html',
    'http://hl7.org/fhir/message-reason-encounter.html',
    'http://hl7.org/fhir/message-significance-category.html',
    'http://hl7.org/fhir/message-transport.html',
    'http://hl7.org/fhir/metric-calibration-state.html',
    'http://hl7.org/fhir/metric-calibration-type.html',
    'http://hl7.org/fhir/metric-category.html',
    'http://hl7.org/fhir/metric-color.html',
    'http://hl7.org/fhir/metric-operational-status.html',
    'http://hl7.org/fhir/missing-tooth-reason.html',
    'http://hl7.org/fhir/claim-modifiers.html',
    'http://hl7.org/fhir/name-use.html',
    'http://hl7.org/fhir/namingsystem-identifier-type.html',
    'http://hl7.org/fhir/namingsystem-type.html',
    'http://hl7.org/fhir/narrative-status.html',
    'http://hl7.org/fhir/network-type.html',
    'http://hl7.org/fhir/note-type.html',
    'http://hl7.org/fhir/nutrition-order-status.html',
    'http://hl7.org/fhir/object-lifecycle.html',
    'http://hl7.org/fhir/object-role.html',
    'http://hl7.org/fhir/object-type.html',
    'http://hl7.org/fhir/observation-category.html',
    'http://hl7.org/fhir/observation-relationshiptypes.html',
    'http://hl7.org/fhir/observation-status.html',
    'http://hl7.org/fhir/operation-kind.html',
    'http://hl7.org/fhir/operation-outcome.html',
    'http://hl7.org/fhir/operation-parameter-use.html',
    'http://hl7.org/fhir/order-status.html',
    'http://hl7.org/fhir/organization-type.html',
    'http://hl7.org/fhir/encounter-participant-type.html',
    'http://hl7.org/fhir/participantrequired.html',
    'http://hl7.org/fhir/participantstatus.html',
    'http://hl7.org/fhir/participationstatus.html',
    'http://hl7.org/fhir/patient-contact-relationship.html',
    'http://hl7.org/fhir/patient-mpi-match.html',
    'http://hl7.org/fhir/payeetype.html',
    'http://hl7.org/fhir/payment-type.html',
    'http://hl7.org/fhir/payment-status.html',
    'http://hl7.org/fhir/practitioner-role.html',
    'http://hl7.org/fhir/practitioner-specialty.html',
    'http://hl7.org/fhir/procedure-progress-status-codes.html',
    'http://hl7.org/fhir/procedure-relationship-type.html',
    'http://hl7.org/fhir/procedure-request-priority.html',
    'http://hl7.org/fhir/procedure-request-status.html',
    'http://hl7.org/fhir/procedure-status.html',
    'http://hl7.org/fhir/process-outcome.html',
    'http://hl7.org/fhir/process-priority.html',
    'http://hl7.org/fhir/property-representation.html',
    'http://hl7.org/fhir/provenance-entity-role.html',
    'http://hl7.org/fhir/provenance-agent-role.html',
    'http://hl7.org/fhir/provenance-agent-type.html',
    'http://hl7.org/fhir/quantity-comparator.html',
    'http://hl7.org/fhir/question-max-occurs.html',
    'http://hl7.org/fhir/questionnaire-answers-status.html',
    'http://hl7.org/fhir/questionnaire-question-control.html',
    'http://hl7.org/fhir/questionnaire-status.html',
    'http://hl7.org/fhir/reaction-event-certainty.html',
    'http://hl7.org/fhir/reaction-event-severity.html',
    'http://hl7.org/fhir/reason-medication-given-codes.html',
    'http://hl7.org/fhir/reason-medication-not-given-codes.html',
    'http://hl7.org/fhir/referencerange-meaning.html',
    'http://hl7.org/fhir/referralstatus.html',
    'http://hl7.org/fhir/relationship.html',
    'http://hl7.org/fhir/remittance-outcome.html',
    'http://hl7.org/fhir/resource-aggregation-mode.html',
    'http://hl7.org/fhir/resource-slicing-rules.html',
    'http://hl7.org/fhir/resource-types.html',
    'http://hl7.org/fhir/resource-validation-mode.html',
    'http://hl7.org/fhir/response-code.html',
    'http://hl7.org/fhir/restful-conformance-mode.html',
    'http://hl7.org/fhir/restful-interaction.html',
    'http://hl7.org/fhir/restful-security-service.html',
    'http://hl7.org/fhir/risk-probability.html',
    'http://hl7.org/fhir/ruleset.html',
    'http://hl7.org/fhir/search-entry-mode.html',
    'http://hl7.org/fhir/search-modifier-code.html',
    'http://hl7.org/fhir/search-param-type.html',
    'http://hl7.org/fhir/search-xpath-usage.html',
    'http://hl7.org/fhir/audit-source-type.html',
    'http://hl7.org/fhir/service-provision-conditions.html',
    'http://hl7.org/fhir/service-referral-method.html',
    'http://hl7.org/fhir/slotstatus.html',
    'http://hl7.org/fhir/special-values.html',
    'http://hl7.org/fhir/specimen-status.html',
    'http://hl7.org/fhir/structure-definition-kind.html',
    'http://hl7.org/fhir/subscription-channel-type.html',
    'http://hl7.org/fhir/subscription-status.html',
    'http://hl7.org/fhir/subscription-tag.html',
    'http://hl7.org/fhir/substance-category.html',
    'http://hl7.org/fhir/supplydelivery-type.html',
    'http://hl7.org/fhir/supplyrequest-kind.html',
    'http://hl7.org/fhir/supplydelivery-status.html',
    'http://hl7.org/fhir/supplyrequest-reason.html',
    'http://hl7.org/fhir/supplyrequest-status.html',
    'http://hl7.org/fhir/testscript-operation-codes.html',
    'http://hl7.org/fhir/timing-abbreviation.html',
    'http://hl7.org/fhir/transaction-mode.html',
    'http://hl7.org/fhir/unknown-content-code.html',
    'http://hl7.org/fhir/vaccination-protocol-dose-status.html',
    'http://hl7.org/fhir/vaccination-protocol-dose-status-reason.html',
    'http://hl7.org/fhir/signature-type.html',
    'http://hl7.org/fhir/versioning-policy.html',
    'http://hl7.org/fhir/vision-base-codes.html',
    'http://hl7.org/fhir/vision-eye-codes.html',
    'http://hl7.org/fhir/xds-relationship-type.html'
]
