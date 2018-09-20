from sqlalchemy_utils import register_composites

from fhir_server.resources.identification.practitioner import Practitioner


class TestPractitioner(object):
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
    address = [{
        "use": "work",
        "text": "text",
        "type": "postal",
        "state": "state",
        "postalCode": "postal code",
        "line": ["line1", "line2"],
        "district": "district",
        "country": "KEN",
        "city": "city",
        "period": {
            "start": "2011-05-24",
            "end": "2011-06-24"
        }
    }]
    gender = 'male'
    birthDate = '1990-11-11'
    photo = None
    role = [{
        "role": {
            "text": "text",
            "coding": [
                {
                    "code": "doctor",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3"
                }]
        },
        "speciality": [{
            "text": "text",
            "coding": [
                {
                    "code": "cardio",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3"
                }]
        }],
    }]
    qualification = [{
        "code": {
            "text": "text",
            "coding": [
                {
                    "code": "100000",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3"
                }]
        },
    }]
    communication = [{
        "text": "text",
        "coding": [
            {
                "code": "en",
                "display": "display",
                "system": "http://testing.test.com",
                "userSelected": "True",
                "version": "2.3"
            }]
    }]

    def test_practitioner_repr(self):
        data = Practitioner(
            id=self.id,
            implicitRules=self.implicitRules,
            language=self.language,
            identifier=self.identifier,
            name=self.name,
            telecom=self.telecom,
            address=self.address,
        )

        assert str(data) == "<Practitioner {}>".format(self.name)

    def test_save_practitioner(self, session):
        data = Practitioner(
            id=self.id,
            implicitRules=self.implicitRules,
            language=self.language,
            identifier=self.identifier,
            active=self.active,
            name=self.name,
            telecom=self.telecom,
            address=self.address,
            gender=self.gender,
            birthDate=self.birthDate,
            photo=self.photo,
            role=self.role,
            qualification=self.qualification,
            communication=self.communication
        )
        session.add(data)
        session.commit()
        register_composites(session.connection())
        get = session.query(Practitioner).first()
        assert get.id == '1'
        assert get.language == 'en'
