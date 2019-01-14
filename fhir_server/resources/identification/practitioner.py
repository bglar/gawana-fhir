from sqlalchemy import Column
from sqlalchemy.orm import validates
from sqlalchemy_utils import CompositeArray as Array

from fhir_server.configs import (
    ADMINISTRATIVE_GENDER_URL,
    PRACTITIONER_ROLE_URL,
    PRACTITIONER_SPECIALITY_URL,
    ANZSCO_OCCUPATIONS_URL,
    LANGUAGE_URI,
)
from fhir_server.elements import primitives, complex
from fhir_server.elements.base.backboneelement import BackboneElement
from fhir_server.resources.domainresource import DomainResource
from fhir_server.elements.base.complex_element import Field


class PractitionerPractitionerRole(BackboneElement):
    """ Roles/organizations the practitioner is associated with.

    The list of roles/organizations that the practitioner is associated with.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field(
                    "organization",
                    {"mini": 0, "maxi": 1},
                    complex.ReferenceField(),
                    "Organization",
                ),
                # Organization where the roles are performed.
                Field(
                    "role", {"mini": 0, "maxi": 1}, complex.CodeableConceptField(), None
                ),
                # Roles which this practitioner may perform.
                Field(
                    "specialty",
                    {"mini": 0, "maxi": -1},
                    complex.CodeableConceptField(),
                    None,
                ),
                # Specific specialty of the practitioner.
                Field(
                    "identifier",
                    {"mini": 0, "maxi": -1},
                    complex.IdentifierField(),
                    None,
                ),
                # Business Identifiers that are specific to a role / location
                Field(
                    "telecom",
                    {"mini": 0, "maxi": -1},
                    complex.ContactPointField(),
                    None,
                ),
                # Contact details that are specific to the role/location/service
                Field("period", {"mini": 0, "maxi": 1}, complex.PeriodField(), None),
                # The period during which the practitioner is authorized
                # to perform in these role(s).
                Field(
                    "location",
                    {"mini": 0, "maxi": -1},
                    complex.ReferenceField(),
                    "Location",
                ),
                # The location(s) at which this practitioner provides care.
                Field(
                    "healthcareService",
                    {"mini": 0, "maxi": -1},
                    complex.ReferenceField(),
                    "HealthcareService",
                )
                # The list of healthcare services that this worker
                # provides for this role's Organization/Location(s).
            ]
        )
        return elm


PractitionerPractitionerRoleField = PractitionerPractitionerRole()


class PractitionerQualification(BackboneElement):
    """ Qualifications obtained by training and certification.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field(
                    "identifier",
                    {"mini": 0, "maxi": -1},
                    complex.IdentifierField(),
                    None,
                ),
                # An identifier for this qualification for the practitioner.
                Field(
                    "code", {"mini": 1, "maxi": 1}, complex.CodeableConceptField(), None
                ),
                # Coded representation of the qualification.
                Field("period", {"mini": 0, "maxi": 1}, complex.PeriodField(), None),
                # Period during which the qualification is valid.
                Field(
                    "issuer",
                    {"mini": 0, "maxi": 1},
                    complex.ReferenceField(),
                    "Organization",
                )
                # Organization that regulates and issues the qualification.
            ]
        )
        return elm


PractitionerQualificationField = PractitionerQualification()


class Practitioner(DomainResource):
    """ A person with a  formal responsibility in the provisioning of
    healthcare or related services.

    A person who is directly or indirectly involved in the provisioning of
    healthcare.
    """

    gender = Column(primitives.CodeField)
    # male | female | other | unknown.

    birthDate = Column(primitives.DateField)
    # The date  on which the practitioner was born.

    active = Column(primitives.BooleanField)
    # Whether this practitioner's record is in active use.

    name = Column(Array(complex.HumanNameField()))
    # A name associated with the person.

    identifier = Column(Array(complex.IdentifierField()))
    # A identifier for the person as this agent.

    telecom = Column(Array(complex.ContactPointField()))
    # A contact detail for the practitioner.

    address = Column(Array(complex.AddressField()))
    # Where practitioner can be found/visited.

    photo = Column(Array(complex.AttachmentField()))
    # Image of the person.

    communication = Column(Array(complex.CodeableConceptField()))
    # A language the practitioner is able to use in patient communication.

    role = Column(Array(PractitionerPractitionerRoleField()))
    # Roles/organizations the practitioner is associated with.

    qualification = Column(Array(PractitionerQualificationField()))
    # Qualifications obtained by training and certification.

    @validates("gender")
    def validate_practitioner_gender(self, key, gender):
        url = ADMINISTRATIVE_GENDER_URL + "?code=" + gender
        self.validate_valuesets(gender, url, "practitioner gender")

        return gender

    @validates("role")
    def validate_practitioner_role(self, key, role):
        for data in role:
            role = data.get("role")
            specialities = data.get("speciality")

            msg1 = "practitioner qualification"
            self.code_fields_validator(specialities, PRACTITIONER_SPECIALITY_URL, msg1)

            msg2 = "practitioner qualification"
            self.code_fields_validator(role, PRACTITIONER_ROLE_URL, msg2)

        return role

    @validates("qualification")
    def validate_qualification(self, key, qualification):
        for data in qualification:
            code = data.get("code")
            msg = "practitioner qualification"
            self.code_fields_validator(code, ANZSCO_OCCUPATIONS_URL, msg)

        return qualification

    @validates("communication")
    def validate_communication(self, key, communication):
        msg = "practitioner communication"
        self.code_fields_validator(communication, LANGUAGE_URI, msg)

        return communication

    def _resource_summary(self):
        summary_fields = ["id", "meta", "identifier", "name"]
        return {"repr": "%r" % self.name, "fields": summary_fields}

    def __repr__(self):
        return "<Practitioner %r>" % self.name
