class MetaOperations(object):
    @classmethod
    def meta_list(cls, **kwargs):
        """
        This operation retrieves a summary of the profiles, tags, and security
        labels for the given scope; e.g. for each scope:
            URL: [base]/$meta - No versionId and lastModified
            URL: [base]/Resource/$meta - No versionId and lastModified
            URL: [base]/Resource/[id]/$meta - Entire Meta

        Out Parameters: {name: return, cardinality: 1..1, Type: Meta}
        :return:
        """
        key = kwargs.get("key")

        def construct_meta(resource, results):
            if results:
                dict_resources = [result._to_dict() for result in results]
                resource_meta = [
                    resource(meta=dict_resource.get("meta"))
                    for dict_resource in dict_resources
                ]

                return resource_meta
            return []

        if key:
            # Return the resource instance meta
            results, count, code = cls.filter(id=key)
            meta = dict(results._to_dict().get("meta"))
            resource_meta = cls(meta=meta)
            return resource_meta, count, code

        else:
            try:
                # A case where resource specific operation is executed
                results, count, code = cls.filter()
                resource_meta = construct_meta(cls, results)
                return resource_meta, count, code

            except AttributeError:
                # A case where operation is executed on all resources
                resource_meta = []

                from fhir_server.resources import all_resources

                for resource in all_resources:
                    results, count, code = resource.filter()
                    data = construct_meta(resource, results)
                    resource_meta.extend(data)

                count = len(resource_meta)
                code = 200
                return resource_meta, count, code

            except Exception as e:
                raise e

    @classmethod
    def meta_add(cls, key, data, **kwargs):
        """
        This operation takes a meta, and adds the profiles, tags, and security
        labels found in it to the nominated resource.

        This operation can also be used on historical entries - to update them
        without creating a different historical version. This operation is
        special in that executing this operation does not cause a new version
        of the resource to be created. The meta is updated directly. This is
        because the content in meta does not affect the meaning of the resource,
        and the security labels (in particular) are used to apply access rules
        to existing versions of resources
            URL: [base]/Resource/[id]/$meta-add

            In Parameters: meta
            Out Parameters: {name: return, cardinality: 1..1, type: meta}

        :param data:
        :param key:
        :return:
        """

        def meta_to_dict(meta_value):
            values = []
            for data in meta_value:
                values.append(dict(data._asdict()))

            return values

        try:
            meta = data.get("meta")
            if meta and (
                meta.get("security") or meta.get("tag") or meta.get("profile")
            ):
                # We only update the meta if either of these values are present
                query, status_code = cls.get_by_id(str(key))
                if query:
                    old_meta_tag = query.meta.tag or []
                    old_meta_security = query.meta.security or []
                    # old_meta_profile = query.meta.profile or []

                    new_meta_tag = meta.get("tag") or []
                    new_meta_security = meta.get("security") or []
                    new_meta_profile = meta.get("profile") or []

                    new_meta_tag.extend(meta_to_dict(old_meta_tag))
                    # new_meta_profile.extend(old_meta_profile)
                    new_meta_security.extend(meta_to_dict(old_meta_security))

                    meta_add = {
                        "tag": new_meta_tag,
                        "profile": new_meta_profile,
                        "security": new_meta_security,
                    }

                    # This update add to the already existing meta properties
                    update, status = cls.update(query, meta=meta_add)
                    meta = dict(update._to_dict().get("meta"))
                    resource_meta = cls(meta=meta)
                    count = len(meta)
                    return resource_meta, count, status_code
                else:
                    raise ValueError(
                        "Resource {}/{} is not known".format(cls.__tablename__, key)
                    )
            else:
                raise ValueError("Meta values are missing to update")

        except Exception as e:
            raise e

    @classmethod
    def meta_delete(cls, key, data, **kwargs):
        """
        This operation takes a meta, and deletes the profiles, tags, and
        security labels found in it from the nominated resource.

        This operation can also be used on historical entries
            URL: [base]/Resource/[id]/$meta-delete

            In Parameters: meta
            Out Parameters: {name: return, cardinality: 1..1, type: meta}

        :param key:
        :return:
        """
        try:
            meta = data.get("meta")
            if meta and (
                meta.get("security") or meta.get("tag") or meta.get("profile")
            ):
                # We only update the meta if either of these values are present
                query, status_code = cls.get_by_id(str(key))
                if query:

                    # This will replace existing meta properties with new ones
                    update, status = cls.update(query, meta=meta)
                    meta = dict(update._to_dict().get("meta"))
                    resource_meta = cls(meta=meta)
                    count = len(meta)
                    return resource_meta, count, status_code
                else:
                    raise ValueError(
                        "Resource {}/{} is not known".format(cls.__tablename__, key)
                    )
            else:
                raise ValueError("Meta values are missing to update")

        except Exception as e:
            raise e
