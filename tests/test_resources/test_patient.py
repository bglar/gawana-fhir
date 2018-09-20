from sqlalchemy_utils import register_composites

from fhir_server.resources.identification.patient import Patient


class TestPatient(object):
    id = "1"
    implicitRules = "https://gawana-fhir.constraints.co.ke/rules"
    language = "en"
    identifier = [{
        "system": "system",
        "use": "secondary",
        "value": "value111",
        "assigner": {
            "reference": "reference url",
            "display": "Patient X"
        },
        "type": {
            "text": "text",
            "coding": [
                {
                    "code": "UDI",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3"
                }]
        },
        "period": {
            "start": "2011-05-24",
            "end": "2011-06-24"
        }
    }]
    active = True
    name = [
        {
            'family': ['family', 'family2'],
            'given': ['given', 'given2'],
            'prefix': ['prefix', 'prefix2'],
            'suffix': ['suffix', 'suffix2'],
            'text': 'family given',
            'use': 'official',
            'period': {
                'start': '2011-05-24',
                'end': '2011-06-24'
            }
        }
    ]
    telecom = [{
        "rank": 2,
        "system": "phone",
        "use": "work",
        "value": "+254712122988",
        "period": {
            "start": "2011-05-24",
            "end": "2011-06-24"
        }
    }]
    gender = 'male'
    birthDate = '1990-11-11'
    deceasedBoolean = False
    deceasedDateTime = None
    address = [{
        "use": "work",
        "text": "text",
        "type": "postal",
        "state": "state",
        "postal_code": "postal code",
        "line": ["line1", "line2"],
        "district": "district",
        "country": "KEN",
        "city": "city",
        "period": {
            "start": "2011-05-24",
            "end": "2011-06-24"
        }
    }]
    maritalStatus = {
        "text": "text",
        "coding": [
            {
                "code": "U",
                "display": "display",
                "system": "http://testing.test.com",
                "userSelected": "True",
                "version": "2.3"
            }]
    }
    multipleBirthBoolean = False
    multipleBirthInteger = 0
    photo = None
    contact = [{
        "relationship": [{
            "text": "text",
            "coding": [
                {
                    "code": "family",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3"
                }]
        }],
        "gender": "male"
    }]
    animal = {
        "breed": {
            "text": "text",
            "coding": [
                {
                    "code": "gsd",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3"
                }]
        },
        "genderStatus": {
            "text": "text",
            "coding": [
                {
                    "code": "intact",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3"
                }]
        },
        "species": {
            "text": "text",
            "coding": [
                {
                    "code": "canislf",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3"
                }]
        }
    }
    communication = [{
        "language": {
            "text": "text",
            "coding": [
                {
                    "code": "en",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3"
                }]
        }
    }]
    careProvider = [{
        "display": "display",
        "reference": "http://spark.furore.com/fhir/Organization/1"
    }]
    managingOrganization = {
        "display": "display",
        "reference": "http://spark.furore.com/fhir/Organization/1"
    }
    link = [{
        "other": {
            "display": "display",
            "reference": "http://spark.furore.com/fhir/Patient/1"
        },
        "type": "replace"
    }]

    def test_patient_repr(self):
        data = Patient(
            id=self.id,
            implicitRules=self.implicitRules,
            language=self.language,
            identifier=self.identifier,
            name=self.name,
            telecom=self.telecom,
            gender=self.gender,
            birthDate=self.birthDate,
            deceasedBoolean=self.deceasedBoolean,
            deceasedDateTime=self.deceasedDateTime,
            address=self.address,
            maritalStatus=self.maritalStatus,
            multipleBirthBoolean=self.multipleBirthBoolean,
            multipleBirthInteger=self.multipleBirthInteger,
            contact=self.contact,
            animal=self.animal,
            communication=self.communication,
            link=self.link,
            managingOrganization=self.managingOrganization,
        )

        assert str(data) == "<Patient {}>".format(self.name)
