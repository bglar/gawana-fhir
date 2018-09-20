import json
import pytest

from fhir_server.resources import Practitioner


class TestPractitionerApis(object):
    PATIENT_URL = '/api/v1/Practitioner'
    meta = {
        "versionId": "13",
        "lastUpdated": "2011-05-24T10:10:10+0300"
    }
    id = '1',
    gender = 'male',
    birthDate = '1990-11-11',
    photo = None,
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

    @pytest.fixture
    def practitioner(self, session):
        data = Practitioner(
            id='1',
            gender='male',
            birthDate='1990-11-11',
            active=True,
            name=self.name,
            meta=self.meta
        )
        session.merge(data)
        session.commit()

    def test_list(self, client, practitioner):
        response = client.get(self.PATIENT_URL)
        data = json.loads(response.get_data().decode('utf8'))
        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 1

    def test_post(self, client):
        records = {
            'gender': 'male',
            'birthDate': '1990-11-11',
            'active': True,
            'name': [
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
        }
        response = client.post(self.PATIENT_URL,
                               content_type='application/json',
                               data=json.dumps(records))
        data = json.loads(response.get_data().decode('utf8'))
        assert response.status_code == 201
        assert data['birthDate'] == '1990-11-11'

    def test_get_detail(self, client, session):
        data = Practitioner(
            id='2',
            gender='male',
            birthDate='1990-11-11',
            active=True,
            name=self.name,
            meta=self.meta
        )
        session.merge(data)
        session.commit()

        get = client.get(self.PATIENT_URL + '/2')
        data = json.loads(get.get_data().decode('utf8'))
        assert get.status_code == 200
        assert data['id'] == '2'
        assert data['birthDate'] == '1990-11-11'

    def test_delete(self, client, session):
        data = Practitioner(
            id='23',
            gender='male',
            birthDate='1990-11-11',
            active=True,
            name=self.name,
            meta=self.meta
        )
        session.merge(data)
        session.commit()
        delete = client.delete(self.PATIENT_URL + '/23',
                               content_type='application/json',
                               data=json.dumps({'gender': 'male'}))
        assert delete.status_code == 200
