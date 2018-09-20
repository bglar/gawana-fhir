import json
import pytest

from fhir_server.resources import Organization


class TestOrganizationApis(object):
    ORG_URL = '/api/v1/Organization'
    meta = {
        "version_id": "1",
        "last_updated": "2011-05-24T10:10:10+0300",
        "profile": [
            "http://example.com/fhir/Patient/",
            "http://example.com/fhir/Organization/"
        ]
    }
    name = 'Test Organization'
    id = '1'
    language = 'EN'
    active = True

    @pytest.fixture
    def new_org(self, session):
        data = Organization(
            id=self.id,
            language=self.language,
            active=self.active,
            name=self.name,
            meta=self.meta
        )
        session.merge(data)
        session.commit()

    def test_list_on_empty_resource(self, client, new_org):
        response = client.get(self.ORG_URL)
        data = json.loads(response.get_data().decode('utf8'))

        assert response.status_code == 200
        assert isinstance(data, list)  # Assert that the response is a list
        assert len(data) == 1  # list

    def test_list_history(self, client):
        response = client.get(self.ORG_URL + '/_history')
        data = json.loads(response.get_data().decode('utf8'))

        assert response.status_code == 200
        assert isinstance(data, list)  # Assert that the response is a list
        assert len(data) == 0  # Empty list

    def test_list_history_on_one_resource(self, client, new_org):
        client.put(self.ORG_URL + '/1',
                   content_type='application/json',
                   data=json.dumps({'name': 'Change Organization'}))

        response = client.get(self.ORG_URL + '/1' + '/_history')
        data = json.loads(response.get_data().decode('utf8'))

        assert response.status_code == 200
        assert isinstance(data, list)  # Assert that the response is a list

    def test_post_ignores_meta_version_and_last_modified(self, client):
        # post some data and assert list has one item
        records = {
            'name': 'Test Organization',
            'meta': self.meta
        }
        response = client.post(self.ORG_URL,
                               content_type='application/json',
                               data=json.dumps(records))
        data = json.loads(response.get_data().decode('utf8'))

        assert response.status_code == 201
        assert isinstance(data, dict)  # Assert that the response is a dict
        assert data['name'] == records['name']
        assert data['meta']['last_updated'] != self.meta['last_updated']

    def test_successful_conditional_create(self, client):
        if_none_exist = {'If-None-Exist': ['name=Savannah']}
        post = client.post(self.ORG_URL,
                           content_type='application/json',
                           data=json.dumps({'name': 'Savannah'}),
                           headers=if_none_exist)
        data = json.loads(post.get_data().decode('utf8'))
        assert post.status_code == 201
        assert data.get('name') == 'Savannah'

    def test_conditional_create_fails_if_one_matching_record_exists(
            self, client, new_org):
        # post a new resource with unique name to query against
        client.post(self.ORG_URL,
                    content_type='application/json',
                    data=json.dumps({'name': 'Kenyatta'}))

        if_none_exist = {'If-None-Exist': ['name=Kenyatta']}
        post = client.post(self.ORG_URL,
                           content_type='application/json',
                           data=json.dumps({'name': 'Kenyatta'}),
                           headers=if_none_exist)
        assert post.status_code == 200

    def test_conditional_create_fails_if_many_matching_record_exists(
            self, client, new_org):
        # post a new resource with unique name to query against
        client.post(self.ORG_URL,
                    content_type='application/json',
                    data=json.dumps({'name': 'Test Organization'}))

        # Now try a conditional POST
        if_none_exist = {'If-None-Exist': ['name=Test Organization']}
        post = client.post(self.ORG_URL,
                           content_type='application/json',
                           data=json.dumps({'name': 'Savannah'}),
                           headers=if_none_exist)
        assert post.status_code == 412

    def test_post_with_single_field(self, client):
        records = {
            'name': 'Test Organization',
        }
        response = client.post(self.ORG_URL,
                               content_type='application/json',
                               data=json.dumps(records))
        data = json.loads(response.get_data().decode('utf8'))
        assert response.status_code == 201
        assert data['name'] == records['name']
        assert data['meta']  # assert that meta was auto-filled

        # content_location has been set
        assert response.headers['Content-Location'] == (
            'http://localhost/api/v1/Organization')

    def test_get_detail(self, client, new_org):
        get = client.get(self.ORG_URL + '/1')
        get_data = json.loads(get.get_data().decode('utf8'))

        assert get.status_code == 200
        assert isinstance(get_data, dict)
        assert get_data['id'] == self.id
        assert get_data['name'] == self.name

    def test_get_by_vid(self, client, new_org):
        get = client.get(self.ORG_URL + '/1/_history/1')

        data = json.loads(get.get_data().decode('utf8'))
        assert get.status_code == 200
        assert data['id'] == self.id
        assert data['name'] == self.name

    def test_etag_header_has_version_id(self, client, new_org):
        get = client.get(self.ORG_URL + '/1')

        assert get.status_code == 200
        assert get.headers['ETag'] == 'w/"1"'  # Assert weak Etag returned
        assert get.headers['Last-Modified']

    def test_get_summary_returns_slim_resource_instance(self, client, new_org):
        # The summary should only include (id, meta, text)
        q_param_text = {'_summary': 'text'}
        q_param_true = {'_summary': 'true'}
        get_text = client.get(self.ORG_URL + '/1', query_string=q_param_text)
        data = json.loads(get_text.get_data().decode('utf8'))
        assert not data.get('language')
        assert data.get('meta')

        get_text = client.get(self.ORG_URL + '/1', query_string=q_param_true)
        data = json.loads(get_text.get_data().decode('utf8'))
        assert not data.get('language')
        assert data.get('meta')

        # The summary should include everything
        q_param_false = {'_summary': 'false'}
        q_param_data = {'_summary': 'data'}
        get_text = client.get(self.ORG_URL + '/1', query_string=q_param_false)
        data = json.loads(get_text.get_data().decode('utf8'))
        assert data.get('language') == 'EN'
        assert data.get('meta')

        get_text = client.get(self.ORG_URL + '/1',
                              query_string=q_param_data)
        data = json.loads(get_text.get_data().decode('utf8'))
        assert data.get('language') == 'EN'
        assert data.get('meta')

    def test_put_detail(self, client, new_org):
        put = client.put(self.ORG_URL + '/1',
                         content_type='application/json',
                         data=json.dumps({'name': 'Change Me'}))

        data = json.loads(put.get_data().decode('utf8'))
        assert put.status_code == 200
        assert data['name'] == 'Change Me'

        # ETag is not still version 1
        assert not(put.headers['ETag'] == 'w/"1"')

    def test_reject_put_if_id_or_param_not_provided(self, client, new_org):
        put = client.put(self.ORG_URL,
                         content_type='application/json',
                         data=json.dumps({'name': 'Change Me'}))

        data = json.loads(put.get_data().decode('utf8'))
        assert put.status_code == 400
        assert data['resourceType'] == 'operationoutcome'

    def test_update_method_not_allowed(self, client, new_org):
        patch = client.patch(self.ORG_URL + '/1',
                             content_type='application/json',
                             data=json.dumps({'name': 'Change Me'}))

        assert patch.status == '405 METHOD NOT ALLOWED'

    def test_update_fails_with_404_if_resource_not_found(
            self, client, new_org):
        put = client.put(self.ORG_URL + '/22',
                         content_type='application/json',
                         data=json.dumps({'name': 'Change Me'}))

        assert put.status == '404 NOT FOUND'

    def test_update_conflict_management_with_if_match(self, client, new_org):
        # At this point version has not changed
        if_match = {'If-Match': '1'}
        put = client.put(self.ORG_URL + '/1',
                         content_type='application/json',
                         data=json.dumps({'name': 'Change Me'}),
                         headers=if_match)
        data = json.loads(put.get_data().decode('utf8'))
        assert put.status_code == 200
        assert data.get('name') == 'Change Me'

        # At this point fails because version changed
        put = client.put(self.ORG_URL + '/1',
                         content_type='application/json',
                         data=json.dumps({'name': 'Change Ya pili'}),
                         headers=if_match)

        data = json.loads(put.get_data().decode('utf8'))
        assert put.status_code == 409
        assert data.get('resourceType') == 'operationoutcome'

    def test_successful_conditional_update(self, client, new_org):
        # post a new resource with unique name to query against
        client.post(self.ORG_URL,
                    content_type='application/json',
                    data=json.dumps({'name': 'AAR'}))

        # Update with some filtering criteria without the id
        q_param = {'name': 'AAR'}
        put = client.put(self.ORG_URL,
                         content_type='application/json',
                         data=json.dumps({'name': 'AAR'}),
                         query_string=q_param)
        data = json.loads(put.get_data().decode('utf8'))
        assert put.status_code == 200
        assert data.get('name') == 'AAR'

    def test_conditional_update_rejected_if_results_is_more_than_one(
            self, client, new_org):
        # Fail if your filtering criteria returns more that one item
        q_param = {'name': 'Test Organization'}
        put = client.put(self.ORG_URL,
                         content_type='application/json',
                         data=json.dumps({'name': 'Savannah'}),
                         query_string=q_param)
        assert put.status == "412 PRECONDITION FAILED"

    def test_conditional_update_rejected_if_no_results_found(
            self, client, new_org):
        # Fail if your filtering criteria returns no items
        q_param = {'name': 'Hakuna Org'}
        put = client.put(self.ORG_URL,
                         content_type='application/json',
                         data=json.dumps({'name': 'Savannah'}),
                         query_string=q_param)
        assert put.status == "404 NOT FOUND"

    # THE FOLLOWING ARE TESTS FOR FAILING CASES
    def test_post_fails_with_no_data(self, client):
        request = client.post(self.ORG_URL, content_type='application/json')
        assert request.status_code == 400

    def test_post_fails_with_invalid_data(self, client):
        records = {
            'namessss': 'Test Organization'
        }
        request = client.post(self.ORG_URL,
                              content_type='application/json',
                              data=json.dumps(records))
        assert request.status == '422 UNPROCESSABLE ENTITY'

    def test_post_fails_if_id_is_provided(self, client):
        records = {
            'id': '122',
            'name': 'Test Organization'
        }
        request = client.post(self.ORG_URL,
                              content_type='application/json',
                              data=json.dumps(records))
        data = json.loads(request.get_data().decode('utf8'))
        assert request.status == '400 BAD REQUEST'
        assert data['resourceType'] == 'operationoutcome'

    def test_get_fails_on_missing_resource(self, client):
        get = client.get(self.ORG_URL + '/10013aghagsy2')
        assert get.status_code == 404

    def test_delete_fails_on_missing_resource(self, client):
        delete = client.delete(self.ORG_URL + '/10013aghagsy2')
        assert delete.status_code == 404

    def test_put_fails_on_missing_resource(self, client):
        put = client.put(self.ORG_URL + '/11',
                         content_type='application/json',
                         data=json.dumps({'name': 'Change Me'}))

        assert put.status_code == 404

    def test_put_fails_on_invalid_resource_data(self, client):
        put = client.put(self.ORG_URL + '/1',
                         content_type='application/json',
                         data=json.dumps({'jina': 'jina'}))

        assert put.status == '422 UNPROCESSABLE ENTITY'

    def test_delete(self, client, new_org):
        delete = client.delete(self.ORG_URL + '/1')

        data = json.dumps(delete.get_data().decode('utf8'))
        assert 'You have deleted the Organization' in str(data)

    @pytest.mark.trylast
    def test_get_deleted_resource_returns_410(self, client, new_org):
        client.delete(self.ORG_URL + '/1')
        get_deleted = client.get(self.ORG_URL + '/1')

        assert get_deleted.status_code == 410

    @pytest.mark.trylast
    def test_get_deleted_version_returns_410(self, client, session):
        client.delete(self.ORG_URL + '/1')
        get_deleted = client.get(self.ORG_URL + '/1/_history/2')

        assert get_deleted.status_code == 404
