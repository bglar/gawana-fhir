import json
import pytest

from fhir_server.resources import HealthcareService


class TestHealthcareServiceApis(object):
    HCS_URL = '/api/v1/HealthcareService'
    meta = {
        "versionId": "13",
        "lastUpdated": "2011-05-24T10:10:10+0300",
        "profile": [
            "http://example.com/fhir/Patient/",
            "http://example.com/fhir/Organization/"
        ]
    }
    id = '1'
    serviceName = 'Test Service'
    comment = 'Some Health care service comment'
    extraDetails = 'extraDetails'

    @pytest.fixture
    def care_service(self, session):
        data = HealthcareService(
            id=self.id,
            comment=self.comment,
            serviceName=self.serviceName,
            extraDetails=self.extraDetails,
            meta=self.meta
        )
        session.merge(data)
        session.commit()

    def test_list(self, client, care_service):
        response = client.get(self.HCS_URL)
        data = json.loads(response.get_data().decode('utf8'))
        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 1

    def test_post(self, client):
        records = {
            'serviceName': 'Test Service',
            'comment': 'Some Health care service comment',
            'extraDetails': 'extraDetails'
        }
        response = client.post(self.HCS_URL,
                               content_type='application/json',
                               data=json.dumps(records))
        data = json.loads(response.get_data().decode('utf8'))
        assert response.status_code == 201
        assert data['comment'] == records['comment']

    def test_get_detail(self, client, care_service):
        get = client.get(self.HCS_URL + '/1')
        data = json.loads(get.get_data().decode('utf8'))
        assert get.status_code == 200
        assert data['id'] == '1'

    def test_put(self, client):
        put = client.put(self.HCS_URL + '/1',
                         content_type='application/json',
                         data=json.dumps({'comment': 'Change Me'}))

        data = json.loads(put.get_data().decode('utf8'))
        assert put.status_code == 200
        assert data['comment'] == 'Change Me'

    def test_delete(self, client):
        delete = client.delete(self.HCS_URL + '/1')
        assert delete.status_code == 200
