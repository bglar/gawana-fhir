from sqlalchemy import Column
from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.orm import validates
from sqlalchemy_utils import CompositeArray as Array

from fhir_server.configs import (
    ADMINISTRATIVE_GENDER_URL,
    MARITAL_STATUS_URL,
    PATIENT_CONTACT_RELATIONSHIP_URL,
    ANIMAL_SPECIES_URL,
    ANIMAL_BREEDS_URL,
    GENDER_STATUS_URL,
    LINK_TYPE_URL,
    LANGUAGE_URI
)
from fhir_server.elements import primitives, complex
from fhir_server.elements.base.backboneelement import BackboneElement
from fhir_server.resources.domainresource import DomainResource
from fhir_server.elements.base.complex_element import Field


class PatientAnimal(BackboneElement):
    """ This patient is known to be an animal (non-human).

    This patient is known to be an animal.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('breed', {'mini': 0, 'maxi': 1},
                  complex.CodeableConceptField(), None),
            # E.g. Poodle, Angus

            Field('genderStatus', {'mini': 0, 'maxi': 1},
                  complex.CodeableConceptField(), None),
            # E.g. Neutered, Intact

            Field('species', {'mini': 1, 'maxi': 1},
                  complex.CodeableConceptField(), None),
            # E.g. Dog, Cow
        ])
        return elm


PatientAnimalField = PatientAnimal()


class PatientCommunication(BackboneElement):
    """ A list of Languages which may be used to communicate with the
    patient about his or her health.

    Languages which may be used to communicate with the patient about his or
    her health.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('language', {'mini': 1, 'maxi': 1},
                  complex.CodeableConceptField(), None),
            # The language which can be used to communicate with the
            # patient about his or her health

            Field('preferred', {'mini': 0, 'maxi': 1},
                  primitives.BooleanField, None),
            # Language preference indicator
        ])
        return elm


PatientCommunicationField = PatientCommunication()


class PatientContact(BackboneElement):
    """ A contact party (e.g. guardian, partner, friend) for the patient.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('relationship', {'mini': 0, 'maxi': -1},
                  complex.CodeableConceptField(), None),
            # The kind of relationship

            Field('name', {'mini': 0, 'maxi': 1},
                  complex.HumanNameField(), None),
            # A name associated with the contact person

            Field('telecom', {'mini': 0, 'maxi': -1},
                  complex.ContactPointField(), None),
            # A contact detail for the person

            Field('address', {'mini': 0, 'maxi': 1},
                  complex.AddressField(), None),
            # Address for the contact person

            Field('gender', {'mini': 0, 'maxi': 1},
                  primitives.CodeField, None),
            # male | female | other | unknown

            Field('organization', {'mini': 0, 'maxi': 1},
                  complex.ReferenceField(), 'Organization'),
            # Organization that is associated with the contact

            Field('period', {'mini': 0, 'maxi': 1},
                  complex.PeriodField(), None),
            # The period during which this contact person or organization
            # is valid to be contacted relating to this patient
        ])
        return elm


PatientContactField = PatientContact()


class PatientLink(BackboneElement):
    """ Link to another patient resource that concerns the same actual person.

    Link to another patient resource that concerns the same actual patient.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('other', {'mini': 1, 'maxi': 1},
                  complex.ReferenceField(), 'Patient'),
            # The other patient resource that the link refers to

            Field('type', {'mini': 1, 'maxi': 1},
                  primitives.CodeField, None),
            # replace | refer | seealso - type of link

        ])
        return elm


PatientLinkField = PatientLink()


class Patient(DomainResource):
    """ Information about an individual or animal receiving health care
    services.

    Demographics and other administrative information about an individual or
    animal receiving care or other health-related services.
    """
    active = Column(primitives.BooleanField)
    # Whether this patient's record is in active use

    gender = Column(primitives.CodeField)
    # male | female | other | unknown

    birthDate = Column(primitives.DateField)
    # The date of birth for the individual

    deceasedBoolean = Column(primitives.BooleanField)
    # Indicates if the individual is deceased or not

    deceasedDateTime = Column(primitives.DateTimeField)
    # Indicates if the individual is deceased or not

    multipleBirthBoolean = Column(primitives.BooleanField)
    # Whether patient is part of a multiple birth

    multipleBirthInteger = Column(primitives.IntegerField)
    # Whether patient is part of a multiple birth

    identifier = Column(Array(complex.IdentifierField()))
    # An identifier for this patient

    name = Column(Array(complex.HumanNameField()))
    # A name associated with the patient

    telecom = Column(Array(complex.ContactPointField()))
    # A contact detail for the individual

    address = Column(Array(complex.AddressField()))
    # Addresses for the individual

    maritalStatus = Column(complex.CodeableConceptField())
    # Marital (civil) status of a patient

    photo = Column(Array(complex.AttachmentField()))
    # Image of the patient

    contact = Column(Array(PatientContactField()))
    # A contact party (e.g. guardian, partner, friend) for the patient

    animal = Column(PatientAnimalField())
    # This patient is known to be an animal (non-human)

    communication = Column(Array(PatientCommunicationField()))
    # A list of Languages which may be used to communicate with the
    # patient about his or her health

    careProvider = Column(Array(complex.ReferenceField()))
    # Patient's nominated primary care provider

    managingOrganization = Column(complex.ReferenceField())
    # Organization that is the custodian of the patient record

    generalPractitioner = Column(Array(complex.ReferenceField()))
    # Patient's nominated primary care provider

    link = Column(Array(PatientLinkField()))
    # Link to another patient resource that concerns the same actual person

    @declared_attr
    def references(self):
        """
        :return:
        Dict. values in the dict should be a | separated string of
        reference resources"""

        return {
            "careProvider": "Organization|Practitioner",
            "managingOrganization": "Organization",
            "generalPractitioner": "Organization|Practitioner"
        }

    @validates('careProvider', 'managingOrganization', 'generalPractitioner')
    def reference_fields(self, key, field):
        """Validates multiple reference fields.

        To add more fields: @validates('field1', 'field2', 'field3')
        And replace the code block before the return statement with:
            ```
            for field_name, reference in self.references.items():
                if key == field_name:
                    self.validate_references(reference, field)
            ```
        """

        for field_name, reference in self.references.items():
            if key == field_name:
                self.validate_references(reference, field)

        return field

    @validates('gender')
    def validate_patient_gender(self, key, gender):
        msg = 'patient gender'
        self.code_fields_validator(gender, ADMINISTRATIVE_GENDER_URL, msg)

        return gender

    @validates('maritalStatus')
    def validate_marital_status(self, key, maritalStatus):
        msg = 'patient marital status code'
        self.code_fields_validator(maritalStatus, MARITAL_STATUS_URL, msg)

        return maritalStatus

    @validates('contact')
    def validate_patient_contact(self, key, contact):
        if contact:
            for data in contact:
                relationships = data.get('relationship')
                gender = data.get('gender')

                msg1 = 'patient contact gender'
                self.code_fields_validator(
                    gender, ADMINISTRATIVE_GENDER_URL, msg1)

                msg2 = 'patient contact relationship'
                self.code_fields_validator(
                    relationships, PATIENT_CONTACT_RELATIONSHIP_URL, msg2)

        return contact

    @validates('animal')
    def validate_animal(self, key, animal):
        if animal:
            species = animal.get('species')
            msg1 = 'patient animal species'
            self.code_fields_validator(species, ANIMAL_SPECIES_URL, msg1)

            breed = animal.get('breed')
            msg2 = 'patient animal breed'
            self.code_fields_validator(breed, ANIMAL_BREEDS_URL, msg2)

            gender_status = animal.get('genderStatus')
            msg3 = 'patient animal gender status'
            self.code_fields_validator(gender_status, GENDER_STATUS_URL, msg3)

        return animal

    @validates('communication')
    def validate_communication(self, key, communication):
        if communication:
            for data in communication:
                language = data.get('language')
                msg = 'patient communication language'
                self.code_fields_validator(language, LANGUAGE_URI, msg)

        return communication

    @validates('link')
    def validate_link(self, key, link):
        if link:
            for data in link:
                link_type = data.get('type')
                msg = 'patient link type'
                self.code_fields_validator(link_type, LINK_TYPE_URL, msg)

        return link

    def _resource_summary(self):
        summary_fields = ['id', 'meta', 'identifier', 'name', ]

        try:
            patient_text = self.name
        except AttributeError:
            patient_text = None
        return {
            'repr': '%r' % patient_text,
            'fields': summary_fields
        }

    def __repr__(self):
        if self.name:
            return '<Patient %r>' % self.name
        else:
            return '<Patient None>'
