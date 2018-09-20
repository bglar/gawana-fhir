from flask import redirect, request

from fhir_server.api import api_v1
from fhir_server.api import response as Response
from fhir_server.operations import BaseOperations
# from .views import resource_list

# Base URLs for cross cutting operations


@api_v1.route('/')
def base_endpoint():
    return redirect('/')


@api_v1.route('/<fhirop:operation>', methods=['GET'])
def base_meta_list_operation(operation):
    """The "base" FHIR `meta-list` operation endpoint.

    These are operations that operate on the full scale of the server.
    For example, "return me all extensions known by this server"
    """
    request_args = dict(request.args)
    base_url = request.base_url
    mime_type = request_args.get('_format') or 'text/html'
    results, count, code = BaseOperations.operation_dispatch(operation)

    return Response.make_data_resp(
        results, 'Parameter', code=code, mime_type=mime_type,
        location=base_url, count=count)
