from datetime import datetime, timezone
from sqlalchemy.sql.expression import text

from fhir_server.configs.database import db


def unpack_resource_helper(resource, resource_instance):
    """
    Creates a valid resource instances with data from raw SQL queries.
    """
    kwargs = {}
    list_data = []

    if not resource_instance:
        return resource()

    if isinstance(resource_instance, list):
        for entry in resource_instance:
            for key in entry.keys():
                if key != "resource_changed":
                    kwargs[key] = entry[key]

                    if isinstance(kwargs[key], tuple):
                        kwargs[key] = dict(kwargs[key]._asdict())

            list_data.append(resource(**kwargs))
        return list_data

    for key in resource_instance.keys():
        if key != "resource_changed":
            kwargs[key] = resource_instance[key]

    return resource(**kwargs)


def tag_summary_resource(instance):
    """Tag a summary resource as `SUBSETTED` for clients.

    Resource that only contains a subset of the data is not suitable for
    use as a base to update the resource, and may not be suitable for
    other uses.

    :param instance:
    :return instance tagged as subset:
    """

    if instance.meta:
        subset = instance.meta._replace(
            tag=[
                {
                    "system": "http://hl7.org/fhir/v3/ObservationValue",
                    "code": "SUBSETTED",
                    "display": "Resource encoded in summary mode",
                }
            ]
        )
        instance.meta = subset
    return instance


class CRUDMixin(object):
    """Provides an easier way of handling the common model operations.

    Simple CRUD(Create, Read, Update, and Delete) is handled here.
    This will also be a utility mixin that handles  most of the http methods
    in the FHIR spec.

    Example usage::
        rsc = ResourceName.create(**(request.data))
        ResourceName.delete(query)
        query = Organization.get_or_404(str(key))
        data = Organization.update(query, **(request.data))
    """

    __table_args__ = {"extend_existing": True}

    @classmethod
    def create(cls, **kwargs):
        """Creates a new record.

        :param kwargs:
        :return The new record:
        """

        # Delete the `resourceType` entry. It is unwanted in the models but
        # client can provide to communicate the resourceType being manipulated
        if "resourceType" in kwargs:
            del kwargs["resourceType"]

        # create resource instance and call save to add to and commit session
        record = cls(**kwargs)
        record.save()
        return record

    @classmethod
    def filter(cls, per_page=30, page=1, **kwargs):
        """A placeholder for resource filtering.

        This should be replaced with a robust search implementation.
        :param page:
        :param per_page:
        :param kwargs:
        """
        # Get rid of params that are not part of the resource fields
        resource_fields = cls.__table__.columns.keys()

        filter_params = {}
        for key, val in kwargs.items():
            if isinstance(val, list):
                filter_params[key] = val[0]
            else:
                filter_params[key] = val

        filter_keys = [param for param in kwargs.keys()]

        for key in filter_keys:
            if key not in resource_fields:
                filter_params.pop(key)

        filter_params["is_deleted"] = False
        count = cls.query.filter_by(**filter_params).count()
        result = (
            cls.query.filter_by(**filter_params).paginate(page, per_page, False).items
        )

        if len(result) > 1:
            # 412 Precondition Failed error indicating the client's
            # criteria were not selective enough
            return result, count, 412

        elif len(result) == 0:
            #  404 Results for supplied params Not Found
            return None, count, 404

        return result[0], count, 200

    @classmethod
    def get_by_id(cls, id, include_deleted=False):
        """
        Select entry by its primary key / Logical id.

        :param include_deleted: It should not query deleted record.
                                Set to True to get all
        :param id: The logical id of the entry
        :return
         result, 200 --> 200 is the HTTP status code that will be accompanied
         with an API response
         None, 410 --> This is returned if the resource was deleted.
         None, 404 --> Not Found:
        """
        result = cls.query.filter_by(id=id, is_deleted=include_deleted).first()

        qq_history = text(
            "SELECT * FROM \"{0}_history\" WHERE (id::text='{1}'::text)".format(
                cls.__tablename__, id
            )
        )
        history_model = db.session.execute(qq_history).first()
        base_deleted = cls.query.filter_by(id=id, is_deleted=True).first()

        if result:
            return result, 200
        elif history_model or base_deleted:
            """This will be interpreted as HTTP_STATUS_CODE 410.
            Means the resource is deleted but it's history exists.
            Returning meta is important to populate Etags and last_modified
            headers for resource contention"""
            result = unpack_resource_helper(cls, history_model)
            return result, 410
        else:
            return None, 404

    @classmethod
    def get_by_vid(cls, vid, key, include_deleted=False):
        """Select entry by its Logical id and resource meta version id.

        :param include_deleted:
        :param vid:
        :param key:
        :return The result:
        """
        qq = text(
            'SELECT * FROM "{0}" WHERE ('
            "(\"{0}\".meta).versionId)::text='{1}'::text AND "
            '"{0}".id::text=\'{2}\'::text AND "{0}".is_deleted={3}'.format(
                cls.__tablename__, vid, key, include_deleted
            )
        )

        qq_history = text(
            'SELECT * FROM "{0}_history" WHERE ('
            "(\"{0}_history\".meta).versionId)::text='{1}'::text AND "
            "\"{0}_history\".id::text='{2}'::text AND "
            '"{0}_history".is_deleted={3}'.format(
                cls.__tablename__, vid, key, include_deleted
            )
        )

        qq_deleted_history = text(
            'SELECT * FROM "{0}_history" WHERE ('
            "(\"{0}_history\".meta).versionId)::text='{1}'::text AND "
            "\"{0}_history\".id::text='{2}'::text AND "
            '"{0}_history".is_deleted=True'.format(cls.__tablename__, vid, key)
        )

        qq_deleted_base = text(
            'SELECT * FROM "{0}" WHERE ('
            "(\"{0}\".meta).versionId)::text='{1}'::text AND "
            '"{0}".id::text=\'{2}\'::text AND "{0}".is_deleted=True'.format(
                cls.__tablename__, vid, key
            )
        )

        base_model = db.session.execute(qq).first()
        history_model = db.session.execute(qq_history).first()
        deleted_base = db.session.execute(qq_deleted_base).first()
        deleted_history = db.session.execute(qq_deleted_history).first()

        if base_model:
            result = unpack_resource_helper(cls, base_model)
            return result, 200
        elif history_model:
            result = unpack_resource_helper(cls, history_model)
            return result, 200
        elif deleted_base:
            # The resource is marked as deleted so return a `401: GONE`
            return deleted_base, 410
        elif deleted_history:
            # The resource is marked as deleted so return a `401: GONE`
            return deleted_history, 410
        else:
            return None, 404

    @classmethod
    def get_summary(cls, id, summary):
        """Get the summary of a resource based on specified summary param.

        :param id:
        :param summary:
        allowed values for summary are:
            `data`: Remove the text element
            `text`: Return only the "text" element, and any mandatory elements
            `count`: Search only: just return a count of the matching resources,
                    without returning the actual matches
            `true`: Return only those elements marked as "summary" in the base
                    definition of the resource(s)
            `false`: Return all parts of the resource(s)

        :return summarised resource instance:
        """
        if summary == "data":
            # Removes the text element
            result, status_code = cls.get_by_id(id)
            result.text = None

            subset = tag_summary_resource(result)
            return subset, status_code

        elif summary == "text":
            # Return only the "text" element, and any mandatory elements
            qq = text(
                'SELECT "{0}".id, "{0}".meta, "{0}".text '
                'FROM "{0}" WHERE "{0}".id::text=\'{1}\'::text '
                'AND "{0}".is_deleted=False'.format(cls.__tablename__, id)
            )
            base_model = db.session.execute(qq).first()

            result = unpack_resource_helper(cls, base_model)
            subset = tag_summary_resource(result)
            return subset, 200

        elif summary == "false":
            # Return all parts of the resource(s)
            result, status_code = cls.get_by_id(id)
            subset = tag_summary_resource(result)
            return subset, status_code

        elif summary == "true":
            # Return only those elements marked as "summary" in the base
            # definition of the resource(s)
            summary_fields = cls._resource_summary(cls)["fields"]
            str_fields = ", ".join(map(str, summary_fields))
            qq = text(
                'SELECT {2} FROM "{0}" WHERE "{0}".id::text=\'{1}\'::text'
                ' AND "{0}".is_deleted=False'.format(cls.__tablename__, id, str_fields)
            )
            base_model = db.session.execute(qq).first()

            result = unpack_resource_helper(cls, base_model)
            subset = tag_summary_resource(result)
            return subset, 200

        result, status_code = cls.get_by_id(id)
        return result, status_code

    @classmethod
    def get_history(cls, key=None, all=False):
        """Get the record history for a resource instance.

        :param key: the logical id of the resource
        :param all: Toggle to get _history of all resources in the system
        :return resource history:
        """
        if key:
            history = text(
                'SELECT * FROM "{0}_history" WHERE "{0}_history".id::text='
                "'{1}' AND is_deleted=False".format(cls.__tablename__, key)
            )

            base = text(
                'SELECT * FROM "{0}" WHERE "{0}".id::text=\'{1}\' AND '
                "is_deleted=False".format(cls.__tablename__, key)
            )

            history_model = db.session.execute(history).fetchall()
            base_model = db.session.execute(base).fetchall()

            history_model.extend(base_model)
        else:
            qq_history = text('SELECT * FROM "{0}_history"'.format(cls.__tablename__))
            history_model = db.session.execute(qq_history).fetchall()

        if history_model:
            result = unpack_resource_helper(cls, history_model)
            return result, 200
        return None, 404

    def update(self, patch=False, **kwargs):
        """Updates a resource instance.

        :param patch: Bool to PATCH on update, default is False (PUT)
        :param kwargs:
        """
        cols = self.__table__.columns.keys()
        col_names = [
            name
            for name in cols
            if name
            not in [
                "id",
                "resource_version",
                "created_at",
                "updated_at",
                "deleted_at",
                "is_deleted",
            ]
        ]

        # Delete the `resourceType` entry. It is unwanted in the models but
        # client can provide to communicate the resourceType being manipulated
        if "resourceType" in kwargs:
            del kwargs["resourceType"]

        for attr, value in kwargs.items():
            # check if updated columns are not in the resource
            # and reject the operation
            assert attr in cols, 'Field "{0}" is not a column in this resource'.format(
                attr
            )

        if patch:
            # PATCH the resource
            for attr, value in kwargs.items():
                setattr(self, attr, value)

        else:
            # PUT the resource
            for col in col_names:
                setattr(self, col, kwargs.get(col))

            # FHIR update through PUT can bring a deleted resource back to life.
            # That is the default behaviour here to mark resource as not
            # deleted. If it is deleted there is a check below to mark it.
            setattr(self, "is_deleted", False)

            if kwargs.get("is_deleted"):
                # These fields are extracted to accommodate most PUT operations.
                # A delete would put `deleted_at` and `is_deleted` so we need
                # to explicitly add them here.
                setattr(self, "is_deleted", kwargs.get("is_deleted"))
                setattr(self, "deleted_at", kwargs.get("deleted_at"))

        self.save()
        return self, 200

    def save(self):
        """
        This is a session mixin through which all session transactions occur.

        This is a way to keep the lifecycle of the session
        (and usually the transaction) separate and external.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception:
            db.session.rollback()
            raise

    def delete(self, delete=True, hard_delete=False):
        """delete a record.

        :param delete: Bool - To soft delete/un-delete a record
        :param hard_delete: Bool - To hard-delete / True delete a record
        """
        # Hard delete
        if hard_delete:
            try:
                db.session.delete(self)
                return db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        # Soft delete
        else:
            now = datetime.now(timezone.utc)
            str_now = datetime.strftime(now, "%Y-%m-%dT%H:%M:%S%z")
            data = {
                "is_deleted": delete,
                "deleted_at": str_now if delete else None,
                "meta": {"lastUpdated": str_now},
            }
            self.update(**data)
        return self, 204
