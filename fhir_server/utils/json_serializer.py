import datetime
import uuid
from inspect import getmembers, ismethod

from flask import json


class ElementSerializer(object):
    """Serialize field data from custom data types.

    Data returned from the database is converted back to our custom composite
    data types. e.g fhir_meta(id=None, extension=(**mode_data)). This result
    is not directly serializable into JSON without using some crazy tricks.
    This mixin abstracts the tricks required for all the composite types created
    in the server
    """

    def _iter_dict(self, data):
        values = data

        if isinstance(values, dict):
            for key, val in values.items():
                if isinstance(val, tuple):
                    values[key] = self._unpack_tuple(val)
                elif isinstance(val, list):
                    for k, v in enumerate(val):
                        val[k] = self._unpack_tuple(v)
                    values[key] = val
                elif isinstance(val, datetime.date):
                    values[key] = val.isoformat()
        return values

    def _unpack_tuple(self, values):
        if isinstance(values, list):
            for val in values:
                dict_data = {name: getattr(val, name) for name in val._fields}
                data = self._unpack_tuple(dict_data)
        elif isinstance(values, str):
            data = values
        elif isinstance(values, datetime.date):
            data = values.isoformat()
        else:
            data = {name: getattr(values, name) for name in values._fields}

        return self._iter_dict(data)

    def _to_dict(self):
        fields = {}

        # This removes unnecessary attributes from a response
        for field in [
            x
            for x, y in getmembers(self)
            if not (ismethod(y))
            and not x.startswith("_")
            and not x.startswith("query")
            and not x.startswith("references")
            and x
            not in [
                "updated_at",
                "is_deleted",
                "deleted_at",
                "resource_version",
                "created_at",
                "metadata",
            ]
        ]:
            values = self.__getattribute__(field)
            if isinstance(values, datetime.date):
                values = values.isoformat()
            elif isinstance(values, uuid.UUID):
                values = str(values)
            if isinstance(values, list):
                for key, val in enumerate(values):
                    if isinstance(val, tuple):
                        values[key] = self._unpack_tuple(val)

            # Deserialize composite types
            if str(values).startswith("fhir_"):
                keys = values._fields
                for key in keys:
                    key_values = values.__getattribute__(key)
                    if isinstance(key_values, list):
                        for val in key_values:
                            if isinstance(val, tuple):
                                attributes = {key: self._unpack_tuple(val)}
                                values = values._replace(**attributes)
                    elif isinstance(key_values, tuple):
                        attributes = {key: self._unpack_tuple(key_values)}
                        values = values._replace(**attributes)
                    elif isinstance(key_values, datetime.date):
                        attributes = {key: key_values.isoformat()}
                        values = values._replace(**attributes)
                values = values._asdict()

            try:
                json.dumps(values)
                fields[field] = values
            except TypeError:
                fields[field] = None

        return fields
