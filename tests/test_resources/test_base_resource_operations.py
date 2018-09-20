import pytest
from fhir_server.resources.resource import Resource


def test_exception_on_unsuccessful_valuesets_request():
    url = "http://www.testfalseurl.com/?false=false"
    with pytest.raises(Exception) as excinfo:
        Resource.validate_valuesets(Resource, url, 'False response')

    assert ('A request to {} returned a'.format(url) in str(excinfo.value) or
            'Max retries exceeded with url:' in str(excinfo.value))
