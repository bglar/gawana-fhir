import json
import pytest

from fhir_server.resources import Location


class TestLocationApis(object):
    LOCATION_URL = '/api/v1/Location'
    meta = {
        "versionId": "13",
        "lastUpdated": "2011-05-24T10:10:10+0300",
        "profile": [
            "http://example.com/fhir/Patient/",
            "http://example.com/fhir/Organization/"
        ]
    }
    id = '1'
    name = 'Nairobi',
    description = 'This is a Community based organization'

    @pytest.fixture
    def location(self, session):
        data = Location(
            id=self.id,
            name=self.name,
            description=self.description,
            meta=self.meta
        )
        session.merge(data)
        session.commit()

    def test_list(self, client, location):
        response = client.get(self.LOCATION_URL)
        data = json.loads(response.get_data().decode('utf8'))
        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 1

    def test_post(self, client):
        records = {
            'name': 'Nairobi',
            'description': "This is a Community based organization"
        }
        response = client.post(self.LOCATION_URL,
                               content_type='application/json',
                               data=json.dumps(records))
        data = json.loads(response.get_data().decode('utf8'))
        assert response.status_code == 201
        assert data['name'] == records['name']

    def test_get_detail(self, client, location):
        get = client.get(self.LOCATION_URL + '/1')
        data = json.loads(get.get_data().decode('utf8'))
        assert get.status_code == 200
        assert data['id'] == '1'

    def test_put_detail(self, client, location):
        put = client.put(self.LOCATION_URL + '/1',
                         content_type='application/json',
                         data=json.dumps({'name': 'Change Me'}))

        data = json.loads(put.get_data().decode('utf8'))
        assert put.status_code == 200
        assert data['name'] == 'Change Me'

    def test_delete(self, client, location):
        delete = client.delete(self.LOCATION_URL + '/1')
        assert delete.status_code == 200
