from sqlalchemy import Column
from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.orm import validates
from sqlalchemy_utils import CompositeArray as Array

from fhir_server.configs import (
    SERVICE_CATEGORY_URL,
    SERVICE_TYPE_URL,
    C80_PRACTICE_CODES_URL,
    SERVICE_PROVISION_CONDITIONS_URL,
    REFERRAL_METHOD_URL,
    DAYS_OF_WEEK)
from fhir_server.elements import primitives, complex
from fhir_server.elements.base.backboneelement import BackboneElement
from fhir_server.resources.domainresource import DomainResource
from fhir_server.elements.base.complex_element import Field


class HealthcareServiceAvailableTime(BackboneElement):
    """ Times the Service Site is available.

    A collection of times that the Service Site is available.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('daysOfWeek', {'mini': 0, 'maxi': -1},
                  primitives.CodeField, None),
            # mon | tue | wed | thu | fri | sat | sun.

            Field('allDay', {'mini': 0, 'maxi': 1},
                  primitives.BooleanField, None),
            # Always available? e.g. 24 hour service.

            Field('availableStartTime', {'mini': 0, 'maxi': 1},
                  primitives.TimeField, None),
            # Opening time of day (ignored if allDay = true).

            Field('availableEndTime', {'mini': 0, 'maxi': 1},
                  primitives.TimeField, None)
            # Closing time of day (ignored if allDay = true).
        ])
        return elm


HealthcareServiceAvailableTimeField = HealthcareServiceAvailableTime()


class HealthcareServiceNotAvailable(BackboneElement):
    """ Not available during this time due to provided reason.

    The HealthcareService is not available during this period of time due to
    the provided reason.
    """
    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('description', {'mini': 1, 'maxi': 1},
                  primitives.StringField, None),
            # Reason presented to the user explaining why time not available.

            Field('during', {'mini': 0, 'maxi': 1},
                  complex.PeriodField(), None)
            # Service not available from this date.
        ])
        return elm


HealthcareServiceNotAvailableField = HealthcareServiceNotAvailable()


class HealthcareService(DomainResource):
    """ The details of a healthcare service available at a location.
    """
    active = Column(primitives.BooleanField)
    # Whether this healthcareservice is in active use

    serviceName = Column(primitives.StringField)
    # Description of service as presented to a consumer while searching.

    comment = Column(primitives.StringField)
    # Additional description and/or any specific issues not covered elsewhere.

    extraDetails = Column(primitives.StringField)
    # Extra details about the service that can't be placed in the other fields.

    eligibilityNote = Column(primitives.StringField)
    # Describes the eligibility conditions for the service.

    programName = Column(Array(primitives.StringField))
    # Program Names that categorize the service.

    publicKey = Column(primitives.StringField)
    # PKI Public keys to support secure communications.

    appointmentRequired = Column(primitives.BooleanField)
    # If an appointment is required for access to this service.

    availabilityExceptions = Column(primitives.StringField)
    # Description of availability exceptions.

    identifier = Column(Array(complex.IdentifierField()))
    # External identifiers for this item.

    providedBy = Column(complex.ReferenceField())
    # Organization that provides this service.

    serviceCategory = Column(complex.CodeableConceptField())
    # Broad category of service being performed or delivered.

    serviceType = Column(Array(complex.CodeableConceptField()))
    # Specific service delivered or performed.

    specialty = Column(Array(complex.CodeableConceptField()))
    # Specialties handled by the HealthcareService

    location = Column(Array(complex.ReferenceField()))
    # Location where service may be provided.

    photo = Column(complex.AttachmentField())
    # Facilitates quick identification of the service.

    telecom = Column(Array(complex.ContactPointField()))
    # Contacts related to the healthcare service.

    coverageArea = Column(Array(complex.ReferenceField()))
    # Location(s) service is inteded for/available to.

    serviceProvisionCode = Column(Array(complex.CodeableConceptField()))
    # Conditions under which service is available/offered.

    eligibility = Column(complex.CodeableConceptField())
    # Specific eligibility requirements required to use the service.

    characteristic = Column(Array(complex.CodeableConceptField()))
    # Collection of characteristics (attributes).

    referralMethod = Column(Array(complex.CodeableConceptField()))
    # Ways that the service accepts referrals.

    notAvailable = Column(Array(HealthcareServiceNotAvailableField()))
    # Not available during this time due to provided reason.

    availableTime = Column(Array(HealthcareServiceAvailableTimeField()))
    # Times the Service Site is available.

    @declared_attr
    def references(self):
        """
        :return:
        Dict. values in the dict should be a | separated string of
        reference resources"""

        return {
            "providedBy": "Organization",
            "location": "Location",
            "coverageArea": "Location"
        }

    @validates('serviceCategory')
    def validate_service_category(self, key, serviceCategory):
        msg = 'service category code'
        self.code_fields_validator(serviceCategory, SERVICE_CATEGORY_URL, msg)

        return serviceCategory

    @validates('serviceType')
    def validate_service_type(self, key, serviceType):
        msg = 'service type code'
        self.code_fields_validator(serviceType, SERVICE_TYPE_URL, msg)

        return serviceType

    @validates('speciality')
    def validate_speciality(self, key, speciality):
        msg = 'service speciality code'
        self.code_fields_validator(speciality, C80_PRACTICE_CODES_URL, msg)

        return speciality

    @validates('serviceProvisionCode')
    def validate_service_provision_code(self, key, serviceProvisionCode):
        msg = 'service provision code code'
        self.code_fields_validator(
            serviceProvisionCode, SERVICE_PROVISION_CONDITIONS_URL, msg)

        return serviceProvisionCode

    @validates('referralMethod')
    def validate_referral_method(self, key, referralMethod):
        msg = 'service referral Method code'
        self.code_fields_validator(referralMethod, REFERRAL_METHOD_URL, msg)

        return referralMethod

    @validates('availableTime')
    def validate_available_time(self, key, availableTime):
        for data in availableTime:
            daysOfWeek = data.get('daysOfWeek')

            for code in daysOfWeek:
                url = DAYS_OF_WEEK + '?code=' + code
                self.validate_valuesets(url, 'service available Time')

        return availableTime

    def _resource_summary(self):
        summary_fields = ['id', 'meta', 'identifier', 'serviceName', ]
        return {
            'repr': '%r' % self.serviceName,
            'fields': summary_fields
        }

    def __repr__(self):
        return '<HealthcareService %r>' % self.serviceName
