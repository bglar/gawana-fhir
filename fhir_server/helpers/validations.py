import requests


def validate_valuesets(code_value, url, response):
    resp = requests.get(url)

    # TODO: Validate the response and fix request on test mocks to
    # accommodate a status_code
    # if not (resp.status_code) == 200:
    #     raise TypeError(
    #         'A request to %s returned a %s status code' % (
    #             url, resp.status_code))

    # TODO optimize this validation
    if 'data' in resp.json():
        for value in resp.json()['data']:
            if value['code'] == code_value:
                return

    raise TypeError(f'The {response} must be defined in {url}')
