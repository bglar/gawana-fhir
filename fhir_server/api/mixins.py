from datetime import datetime, timezone

from flask import request, views
from flask_sqlalchemy import _BoundDeclarativeMeta
from werkzeug.http import HTTP_STATUS_CODES

from fhir_server.api import response as Response
from fhir_server.configs import ITEMS_PER_PAGE
from fhir_server.resources import all_resources


class BaseApi(object):
    resource = None

    def get_resource(self):
        assert self.resource is not None, (
            "{0} should include a `resource` attribute".format(
                self.__class__.__name__)
        )

        assert isinstance(self.resource, _BoundDeclarativeMeta), (
            "Ensure that the resource attribute is a Model instance"
        )

        resource = self.resource
        return resource


def add_meta_last_modified(data):
    now = datetime.now(timezone.utc)
    str_now = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S%z')
    if not data.get('meta'):
        data['meta'] = {}
    data['meta']['lastUpdated'] = str_now
    return data


def validate_resource_type(request_data, location, mime_type):
    resource_type = request_data.get('resourceType')
    resource_names = [
        resource.__tablename__.lower() for resource in all_resources]
    response = None

    if not resource_type:
        err = ("Failed to parse request body as resource. Error was: "
               "Invalid content detected, missing required element: "
               "'resourceType'")
        response = Response.log_operation_outcome(
            [location], code='invalid', diagnostics=err,
            mime_type=mime_type, status_code=400)
    else:
        err = ("Failed to parse request body as resource. Error was: "
               "Incorrect resource type {0} found, expected "
               "{1}".format(resource_type, location))

        if not (resource_type.lower() in resource_names):
            response = Response.log_operation_outcome(
                [location], code='invalid', diagnostics=err,
                mime_type=mime_type, status_code=404)

    return response


class ListMixin(BaseApi, views.MethodView):
    """return a list of resource instances"""

    # @requires_auth
    def get(self):
        location = request.full_path
        base_url = request.base_url

        resource = self.get_resource()
        request_args = dict(request.args)
        mime_type = request_args.get('_format') or 'text/html'

        # PAGINATION PARAMS
        count = None  # initialize the count for objects
        try:
            page = int(request_args.get('_page')[0])
        except TypeError:
            page = 1

        try:
            per_page = int(request_args.get('_count')[0])
        except TypeError:
            per_page = ITEMS_PER_PAGE

        if str(location).endswith('_history/'):
            query, status_code = resource.get_history()
        else:
            query, count, status_code = resource.filter(
                page=page, per_page=per_page, **request_args)

        return Response.make_data_resp(
            query, resource, code=200, mime_type=mime_type, location=base_url,
            count=count
        )


class CreateMixin(BaseApi, views.MethodView):
    """create a new resource instance."""

    def post(self, key=None, operation=None):
        """
        The key and/or op are only required when an operation is executed.

        :param key: Resource logicalID
        :param operation: Operation associated with the resources
        :return:
        """
        resource = self.get_resource()
        location = request.full_path
        base_url = request.base_url

        request_args = dict(request.args)
        mime_type = request_args.get('_format') or 'text/html'
        if_none_exist = request.headers.get('If-None-Exist')

        if validate_resource_type(request.data, location, mime_type):
            return validate_resource_type(request.data, location, mime_type)

        if operation:
            # We take this path to perform an operation on the resource.
            # The operation here can be resource specific of cross cutting all
            # resources
            try:
                data = request.data
                op_response, count, code = resource.operation_dispatch(
                    op=operation, key=key, data=data)

                return Response.make_data_resp(
                    op_response, resource, code=code, mime_type=mime_type,
                    location=location)

            except Exception as e:
                return Response.log_operation_outcome(
                    [location], code='invalid', diagnostics=e,
                    status_code=400, mime_type=mime_type)

        if if_none_exist:
            # For conditional create, use filtering as an identification
            # criteria for an existing record of the resource instance.
            # Filtering params should be provided in the request header
            query_param = {}
            key, val = if_none_exist.split('=')
            query_param[key] = val

            query, count, status_code = resource.filter(**query_param)
            if status_code != 404:
                # 404 here means the filter had no match so a new record will
                # not be a duplicate

                err = 'Resource matching the given params already exists'
                return Response.log_operation_outcome(
                    [location], code='invalid', diagnostics=err,
                    status_code=status_code, mime_type=mime_type)

        if not request.data:
            err = 'No data provided.' \
                  'You cannot create an empty resource instance.'
            return Response.log_operation_outcome(
                [location], code='invalid', diagnostics=err,
                mime_type=mime_type)

        if request.data.__contains__('id'):
            id = request.data['id']
            err = 'Can not create resource with ID {0}, ID must not be ' \
                  'supplied on a create (POST) operation.'.format(id)
            return Response.log_operation_outcome(
                [location + id], code='invalid', diagnostics=err,
                status_code=400, mime_type=mime_type)

        try:
            request_data = add_meta_last_modified(request.data)
            data = resource.create(**request_data)
        except Exception as e:
            return Response.log_operation_outcome(
                [location], code='invalid', status_code=422,
                diagnostics=e.args, severity='fatal', mime_type=mime_type)

        return Response.make_data_resp(
            data, resource, code=201, mime_type=mime_type, location=base_url)


class RetrieveMixin(BaseApi, views.MethodView):
    """expose a single resource instance."""

    def get(self, key, vid=None):
        resource = self.get_resource()
        location = request.full_path
        base_url = request.base_url

        request_args = dict(request.args)
        mime_type = request_args.get('_format') or 'text/html'

        # Summary defaults to False/Data and returns the full resource
        summary = request_args.get('_summary')

        if vid:
            query, status_code = resource.get_by_vid(str(vid), str(key))
        elif summary and not vid:
            # Summary responses are not allowed if resource instance
            # version is required. Return a summary of the resource
            query, status_code = resource.get_summary(str(key), summary[0])
        elif str(location).endswith('_history'):
            query, status_code = resource.get_history(key=key)
        else:
            query, status_code = resource.get_by_id(str(key))

        if not query:
            err = '{0}/{1}/_history/{2} is not known'.format(
                resource.__tablename__.title(), key,
                vid) if vid else '{0}/{1} is not known'.format(
                resource.__tablename__.title(), key)

            return Response.log_operation_outcome(
                [location], code='invalid', diagnostics=err,
                status_code=status_code, mime_type=mime_type
            )

        elif status_code == 410:
            err = '{0}/{1} is a Deleted Resource Instance'.format(
                resource.__tablename__, key)
            return Response.log_operation_outcome(
                [location], code='invalid', diagnostics=err,
                mime_type=mime_type, status_code=status_code)

        return Response.make_data_resp(query, resource, code=status_code,
                                       mime_type=mime_type, location=base_url)


class DestroyMixin(BaseApi, views.MethodView):
    """delete a single resource instance."""

    def delete(self, key=None):
        resource = self.get_resource()
        location = request.full_path

        request_args = dict(request.args)
        mime_type = request_args.get('_format') or 'text/html'

        # For conditional Deletes, use filtering as an identification criteria
        # for an existing record of the resource instance.
        if not key:
            if not len(request_args) > 0:
                err = 'Logical ID or QueryParam(for conditional deletes) ' \
                      'not provided '
                return Response.log_operation_outcome(
                    location=location, code='invalid', diagnostics=err,
                    mime_type=mime_type)

            query, count, status_code = resource.filter(**request_args)
            if status_code != 200:
                return Response.log_operation_outcome(
                    [location], diagnostics=HTTP_STATUS_CODES.get(status_code),
                    status_code=status_code, mime_type=mime_type)

        else:
            query, status_code = resource.get_by_id(str(key))

        if not query:
            err = '{0}/{1}/ is not known'.format(
                resource.__tablename__, key)
            return Response.log_operation_outcome(
                [location + 'id'], code='invalid', diagnostics=err,
                mime_type=mime_type, status_code=status_code)

        try:
            response, status_code = resource.delete(query)
        except Exception as e:
            return Response.log_operation_outcome(
                [location], code='invalid', mime_type=mime_type,
                diagnostics=e.args, severity='fatal', status_code=status_code)

        return Response.log_operation_outcome(
            [location], severity='information', diagnostics='GONE',
            status_code=status_code, mime_type=mime_type,
            query_result=response)


class UpdateMixin(BaseApi, views.MethodView):
    def put(self, key=None, vid=None):
        """update a single resource instance.

        The key is instantiated to none because of conditional updates
        or creates that supply query params. We use the results of the
        query param to get the resource instance id
        """
        resource = self.get_resource()
        location = request.full_path
        base_url = request.base_url

        request_args = dict(request.args)
        mime_type = request_args.get('_format') or 'text/html'

        if validate_resource_type(request.data, location, mime_type):
            return validate_resource_type(request.data, location, mime_type)

        if not request.data or (len(request.data) == 0):
            err = 'No data provided.' \
                  'You cannot update resource instance without field data.'
            return Response.log_operation_outcome(
                [location], code='invalid', mime_type=mime_type,
                diagnostics=err)

        # For conditional updates, use filtering as an identification criteria
        # for an existing record of the resource instance.
        if not key:
            if not len(request_args) > 0:
                err = 'Logical ID or QueryParam(for conditional updates) ' \
                      'not provided '
                return Response.log_operation_outcome(
                    location=location, code='invalid', diagnostics=err,
                    mime_type=mime_type)

            query, count, status_code = resource.filter(**request_args)
            if status_code != 200:
                return Response.log_operation_outcome(
                    [location], diagnostics=HTTP_STATUS_CODES.get(status_code),
                    status_code=status_code, mime_type=mime_type)

        else:
            query, status_code = resource.get_by_id(str(key))

        if query and vid:
            # For updates through a history endpoint we need to confirm that
            # the queried resource version is the current version
            resource_version = query.meta.versionId
            if not resource_version == vid:
                err = ('Trying to update {}/{}/_history/{} but this is not the '
                       'current version'.format(resource.__tablename__,
                                                key, vid))
                return Response.log_operation_outcome(
                    [location], diagnostics=err, status_code=400,
                    mime_type=mime_type)

        if not query:
            err = 'The {0} is an Unknown Resource Instance'.format(
                resource.__tablename__)
            return Response.log_operation_outcome(
                [location + 'id'], code='invalid', diagnostics=err,
                mime_type=mime_type, status_code=status_code)

        if_match = request.headers.get('If-Match')
        etag = query.meta.versionId

        if if_match:
            if if_match != etag:
                err = 'CONFLICT. The resource instance version Changed'
                return Response.log_operation_outcome(
                    [location + 'id'], code='invalid', diagnostics=err,
                    mime_type=mime_type, status_code=409)
        else:
            err = 'Pre-condition failed. An If-Match header should ' \
                  'be provided for resource updates'
            return Response.log_operation_outcome(
                [location + 'id'], code='invalid', diagnostics=err,
                mime_type=mime_type, status_code=412)

        try:
            request_data = add_meta_last_modified(request.data)
            data, status_code = resource.update(query, **request_data)
        except Exception as e:
            return Response.log_operation_outcome(
                [location], code='invalid', diagnostics=e.args,
                severity='fatal', mime_type=mime_type, status_code=422)
        else:
            if status_code != 200:
                Response.log_operation_outcome(
                    [location], diagnostics=HTTP_STATUS_CODES[status_code],
                    status_code=status_code, mime_type=mime_type)

        return Response.make_data_resp(data, resource, code=200,
                                       mime_type=mime_type, location=base_url)
