import json
import pytest

from fhir_server.resources import Patient


class TestPatientApis(object):
    PATIENT_URL = '/api/v1/Patient'
    meta = {
        "versionId": "13",
        "lastUpdated": "2011-05-24T10:10:10+0300",
        "profile": [
            "http://example.com/fhir/Patient/",
            "http://example.com/fhir/Organization/"
        ]
    }
    id = '1'
    active = True,
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
    def patient(self, session):
        data = Patient(
            id=self.id,
            active=self.active,
            meta=self.meta
        )
        session.merge(data)
        session.commit()

    def test_list(self, client, patient):
        response = client.get(self.PATIENT_URL)
        data = json.loads(response.get_data().decode('utf8'))
        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 1

    def test_post(self, client):
        records = {
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
        assert data['active']

    def test_get_detail(self, client, patient):
        get = client.get(self.PATIENT_URL + '/1')
        data = json.loads(get.get_data().decode('utf8'))
        assert get.status_code == 200
        assert data['id'] == '1'

    def test_put_detail(self, client, patient):
        put = client.put(self.PATIENT_URL + '/1',
                         content_type='application/json',
                         data=json.dumps({'active': False}))

        data = json.loads(put.get_data().decode('utf8'))
        assert put.status_code == 200
        assert data['active'] is False

    def test_delete(self, client, patient):
        delete = client.delete(self.PATIENT_URL + '/1',
                               content_type='application/json',
                               data=json.dumps({'active': True}))
        assert delete.status_code == 200
