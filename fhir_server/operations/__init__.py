from .metaops import MetaOperations


class BaseOperations(MetaOperations):
    """
    A proxy for base resource operations.

    This brings together operations that cut across all FHIR resources
    """

    @classmethod
    def operation_dispatch(cls, op, key=None, data=None):
        """A dispatch method.

        Forwards request to methods based on the op params.
        :param key:
        :param data:
        :param op:
        :return:
        """
        operation_name = op.replace('-', '_')

        if operation_name == 'meta':
            # This is only important because all resources have attribute meta
            # which will conflict with the `meta` operation and make it
            # impossible to dynamically call the operation
            operation_name = 'meta_list'

        try:
            method = getattr(cls, operation_name)
        except Exception:
            raise AttributeError(
                '{} is not a valid operation for this Resource'.format(op))

        return method(data=data, key=key)
