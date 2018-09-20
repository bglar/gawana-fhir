import sys
import os
import json
from dateutil import tz, parser
import traceback
from xml.etree import ElementTree

from flask import current_app, Response, make_response
import xmltodict

from fhir_server.configs import VALID_JSON_MIMETYPES, VALID_XML_MIMETYPES
from fhir_server.resources import OperationOutcome

"""
Helper for making API returns consistent
"""

success_codes = [200, 201, 204]


def clean_dict(data):
    """
    Removed dict entries with None values or empty dicts.
    :param data:
    :return:
    """
    list_data = []

    def sweep(sweep_data):
        dict_data = {}
        for key, val in sweep_data.items():
            if isinstance(val, dict):
                val = clean_dict(val)
            elif isinstance(val, list):
                for k, entry in enumerate(val):
                    val[k] = clean_dict(entry)

            if (val is not None) and val != {}:
                dict_data[key] = val
        return dict_data

    if isinstance(data, dict):
        return sweep(data)

    elif isinstance(data, list):
        for entry in data:
            list_data.append(sweep(entry))
        return list_data

    return data


def _response_to_xml(data):
    """
    This converts json data to xml.

    :param data:
    data comes in as dict:
    ```{
        'resourceType': 'Organization',
        'id': '31ea4cc8-14cd-411c-adca-fe19bcecb87a',
        'meta': {
            'last_updated': 'Thu, 04 Aug 2016 15:13:29 GMT',
            'version_id': '4'
        },
        'name': 'Karen',
        'part_of': {
            'display': 'display',
            'reference': 'http://spark.furore.com/fhir/Organization/1'
        }
    }```
    and is converted to this:
    # (to make the process of parsing from json to xml less painful)
    ```{
        'Organization': {
            '@xmlns': 'http://hl7.org/fhir',
            'id': {'@value': '31ea4cc8-14cd-411c-adca-fe19bcecb87a'},
            'meta': {
                'last_updated': {'@value': 'Thu, 04 Aug 2016 15:13:29 GMT'},
                'version_id': {'@value': '4'}
            },
            'name': {'@value': 'Karen'},
            'part_of': {
                'display': {'@value': 'display'},
                'reference': {
                    '@value': 'http://spark.furore.com/fhir/Organization/1'}
            }
        }
    }```

    :return: xml-parsed data
    """
    def add_values_and_elements_to_dict(dict_data):
        # to_xml = dict_data
        if isinstance(dict_data, list):
            for data in dict_data:
                add_values_and_elements_to_dict(data)

        elif isinstance(dict_data, dict):
            for key, value in dict_data.items():
                if isinstance(value, dict):
                    if not hasattr(value, '@value'):
                        add_values_and_elements_to_dict(value)

                elif isinstance(value, list):
                    for val in value:
                        add_values_and_elements_to_dict(val)

                else:
                    #  We add this to make it easy for fhir xml formatting
                    dict_data[key] = {'@value': value}

            # to_xml['@xmlns'] = 'http://hl7.org/fhir'  # Add additional tags
        return dict_data

    resource_dict = add_values_and_elements_to_dict(data)

    # create a temporary bundle
    if isinstance(resource_dict, list):
        resource_list = []
        for data in resource_dict:
            resource_type = str(
                data.pop('resourceType')['@value']).title()

            data['@xmlns'] = "http://hl7.org/fhir"
            resource = {
                'resource': {
                    resource_type: data
                }
            }
            resource_list.append(resource)
        resource_xml = xmltodict.unparse(
            {
                'Bundle': {
                    '@xmlns': 'http://hl7.org/fhir',
                    'entry': resource_list
                }
            }
        )
    else:
        # remove the resourceType from xml and make it the xml root
        resource_type = str(
            resource_dict.pop('resourceType')['@value']).title()
        resource_dict['@xmlns'] = 'http://hl7.org/fhir'  # Add additional tags
        resource_xml = xmltodict.unparse({resource_type: resource_dict})

    ElementTree.register_namespace('', 'http://hl7.org/fhir')
    resource_xml = ElementTree.tostring(ElementTree.fromstring(resource_xml))

    return resource_xml.decode('utf-8')


def _make_response(response, code=200, mime_type='text/html', **kwargs):
    """
     This is an example response header that we should aim at constructing for
     the responses in this method.
        Single resource:
            HTTP/1.1 200 OK
            Cache-Control: no-cache
            Pragma: no-cache
            Content-Type: application/xml+fhir; charset=utf-8
            Content-Location: Organization/1/_history/spark11
            Expires: -1
            Last-Modified: Wed, 06 Jan 2016 12:01:25 GMT
            ETag: W/"spark11"
            Server: Microsoft-IIS/8.5
            Date: Wed, 20 Jul 2016 10:05:12 GMT
            Content-Length: 810

        Multiple Resources:
            HTTP/1.1 200 OK
            Cache-Control: no-cache
            Pragma: no-cache
            Content-Type: application/xml+fhir; charset=utf-8
            Expires: -1
            Server: Microsoft-IIS/8.5
            Date: Fri, 22 Jul 2016 07:41:49 GMT
            Content-Length: 31417

    My response:
        HTTP/1.0 200 OK
        Content-Type: application/xml; charset=utf-8
        Content-Length: 700
        Last-Modified: 2016-07-21 15:34:48+00:00
        ETag: w/"63"
        Server: Werkzeug/0.11.3 Python/3.5.1
        Date: Thu, 21 Jul 2016 15:46:27 GMT
    """
    if not response:
        response = []

    response_data = clean_dict(response)

    content_location = kwargs.get('location')
    query_result = kwargs.get('query_result')
    count = kwargs.get('count')

    if query_result:
        query_result_dict = query_result._to_dict()
        query_meta = query_result_dict.get('meta')
    else:
        query_meta = query_result

    if isinstance(response_data, list):
        # Temporary mechanism to bundle results before bundle resource come in
        # for resource in response_data:
        data = [{'resource': resource} for resource in response_data]
        response_data = {
            'resourceType': 'Bundle',
            'total': count,
            'entry': data
        }

    if str(mime_type[0]) in VALID_XML_MIMETYPES:
        mime_type = 'application/xml'
        response_data = _response_to_xml(response_data)
        api_response = Response(response_data, code, mimetype=mime_type,
                                content_type=mime_type)
    elif str(mime_type[0]) in VALID_JSON_MIMETYPES:
        mime_type = 'application/json'
        response_data = json.dumps(response_data)
        api_response = Response(response_data, code, mimetype=mime_type,
                                content_type=mime_type)

    else:
        api_response = make_response(response_data, code)

    if code not in success_codes:
        return api_response

    if isinstance(response, dict):
        meta = dict(response).get('meta') or query_meta

        if meta:

            str_time = meta.get('lastUpdated')
            last_modified = parser.parse(str_time)
            gmt = last_modified.replace(tzinfo=tz.gettz('GMT'))
            f_last_modified = gmt.strftime('%a, %d %b %Y %X %Z')

            etag = meta.get('versionId')
            if content_location:
                # The content location for a deleted resource is None. We do
                # not need to append the history to a NoneType. It will Blow up.
                content_location += '_history/{}'.format(etag)

            api_response.headers['Last-Modified'] = f_last_modified
            api_response.headers['ETag'] = 'w/"{0}"'.format(etag)

    api_response.headers['Content-Type'] = '{}; charset=utf-8'.format(mime_type)
    api_response.headers['Content-Location'] = content_location

    return api_response


def make_data_resp(data, resource, code=200, mime_type='text/html', **kwargs):
    if data:
        if isinstance(data, list):
            data = [entry._to_dict() for entry in data]
            for record in data:
                if not isinstance(resource, str):
                    record['resourceType'] = resource.__tablename__
                else:
                    record['resourceType'] = resource

        else:
            data = data._to_dict()
            data['resourceType'] = resource.__tablename__

    return _make_response(data, code=code, mime_type=mime_type, **kwargs)


def make_error_resp(error, msg=None, code=400, mime_type='text/html'):
    log = error
    try:
        log = error._to_dict()
    except AttributeError:
        log = log
    finally:
        response = {
            'OperationOutcome': log,
            'DEBUG_LOG': msg
        }
    return _make_response(response, code=code, mime_type=mime_type)


def make_exception_resp(exception, code=422, mime_type='text/html'):
    """Include file name, line number and stacktrace.

    NOTE: Will probably not want to display exceptions to users in production

    :param exception:
    :param type:
    :param code:
    :return:
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    msg = "Excpetion: %s: %s: %s %s" % (
        exc_type, file_name, exc_tb.tb_lineno, traceback.format_exc())

    if current_app.config['DEBUG']:
        return make_error_resp(exception, msg=msg,
                               code=code, mime_type=mime_type)
    else:
        current_app.logger.critical('Exception caught:  %s' % msg)
        return make_error_resp(exception, code=code, mime_type=mime_type)


def log_operation_outcome(location, code=None, severity='error',
                          diagnostics=None, expression=None, details=None,
                          mime_type='application/json', status_code=400,
                          query_result=None):
    """
    All Error/Exceptions/Responses are logged to an OperationOutcome Resource.

    :param location:
    :param code:
    :param severity:
    :param diagnostics:
    :param expression:
    :param details:
    :param mime_type:
    :param status_code: HTTP status code
    :param query_result: Result from an initial query to provide information
                        e.g meta versioning on deleting a resource.ss
    :return operation outcome instance:
    """
    data = {
        "issue": [{
            "severity": severity,
            "code": code,
            "diagnostics": "{}".format(diagnostics),
            "location": location,
            "expression": expression,
            "details": details
        }],
        "text": {
            "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><h1>Operation "
                   "Outcome</h1><p>{}</p></div>".format(diagnostics),
            'status': 'generated'
        }
    }
    try:
        outcome_response = OperationOutcome.create(**data)
    except Exception as e:
        return make_exception_resp(e.args, code=status_code,
                                   mime_type=mime_type)

    return make_data_resp(outcome_response, OperationOutcome, code=status_code,
                          mime_type=mime_type, query_result=query_result)
