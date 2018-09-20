-- Register db level constraints in this file.
--
-- It should be executed after the migrations have been run. n/b a hook
-- should be added to automatically generate and add these constraints
-- whenever alembic is executed to make model migrations i.e if migrations
-- involves adding a new schema to the database

-- This checks that atleast one column is present in an Array field if the
-- parent/complex column is profiled to One-to-Many. This function accepts
-- variable numbers and arguments.

DROP FUNCTION IF EXISTS count_not_nulls(VARIADIC p_array anyarray) CASCADE;
CREATE FUNCTION count_not_nulls(VARIADIC p_array anyarray) RETURNS NUMERIC AS
$$
    SELECT count(x) FROM unnest($1) AS x
$$ LANGUAGE SQL IMMUTABLE;

ALTER TABLE "Organization"
ADD CONSTRAINT chk_only_one_is_not_null CHECK(count_not_nulls(
    identifier::text, address::text, contact::text) = 1);


-- The following are unique indices for resources
DROP FUNCTION IF EXISTS unpack_and_add_index(fhir_identifier[], text) CASCADE;
CREATE OR REPLACE FUNCTION unpack_and_add_index(fhir_identifier[], schema_name text)
RETURNS text AS
$$
    DECLARE
        ctype fhir_identifier;
        iterator integer := 0;
    BEGIN
        FOREACH ctype IN ARRAY $1
        LOOP
            EXECUTE 'DROP INDEX IF EXISTS ' || schema_name || '_identifier_value_' || iterator ||;

            EXECUTE 'CREATE UNIQUE INDEX ' || schema_name || '_identifier_value_' || iterator ||
                    ' ON ' || schema_name || ' (((composite_type[' || iterator ||']).value));';

            iterator = iterator + 1;
        END LOOP;
        RETURN schema_name;
    END;
$$ LANGUAGE plpgsql;

ALTER TABLE "Organization"
DROP CONSTRAINT IF EXISTS chk_unique_identifier_value;

ALTER TABLE "Organization"
ADD CONSTRAINT chk_unique_identifier_value CHECK(unpack_and_add_index(
    identifier::fhir_identifier[], "organization"::text) = 'organization');

DROP INDEX IF EXISTS organisation_meta_version_id;
CREATE UNIQUE INDEX organisation_meta_version_id ON Organization (
    ((meta).versionId));

------------------------------------------------------------------------------
--------------- Check versionID for Optimistic Concurrency Control -----------
CREATE OR REPLACE FUNCTION meta_version_id_concurrency()
RETURNS trigger AS
$meta_version_id_concurrency$
    DECLARE

        new_version text := (NEW.meta).versionId;
        old_version text;
        rec fhir_meta;
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            new_version := NEW.resource_version;

            rec := ((NEW.meta).id, (NEW.meta).extension, new_version, (NEW.meta).lastUpdated,
                (NEW.meta).profile, (NEW.meta).security, (NEW.meta).tag);
            NEW.meta := rec;
            RETURN NEW;

        ELSIF (TG_OP = 'UPDATE') THEN
            IF (OLD.meta).versionId IS NULL THEN
                new_version := NEW.resource_version;

                rec := ((NEW.meta).id, (NEW.meta).extension, new_version, (NEW.meta).lastUpdated,
                    (NEW.meta).profile, (NEW.meta).security, (NEW.meta).tag);
                NEW.meta := rec;
                RETURN NEW;

            ELSE
                old_version := (OLD.meta).versionId;
                IF old_version != new_version THEN
                    RAISE EXCEPTION 'Update of versionId: % -> % not allowed. The versionId has changed', old_version, new_version;
                ELSE
                    new_version := NEW.resource_version;

                    rec := ((NEW.meta).id, (NEW.meta).extension, new_version, (NEW.meta).lastUpdated,
                            (NEW.meta).profile, (NEW.meta).security, (NEW.meta).tag);
                    NEW.meta := rec;
                    RETURN NEW;
                END IF;
            END IF;
        END IF;
    END;
$meta_version_id_concurrency$ LANGUAGE plpgsql;

-- Trigger executed before insert/update for resources to validate meta
CREATE TRIGGER meta_version_id_concurrency BEFORE INSERT OR UPDATE ON "Organization"
    FOR EACH ROW EXECUTE PROCEDURE meta_version_id_concurrency();


------------------------------------------------------------------------------
-------- Database level constraints for Meta fields --------------------------

CREATE OR REPLACE FUNCTION validate_meta_fields()
RETURNS TRIGGER AS
$validate_meta_fields$
    DECLARE
        field_name text := TG_ARGV[0];
        mini text := TG_ARGV[1];
        maxi text := TG_ARGV[2];

    BEGIN
        IF field_name = 'versionId' THEN
            IF (NEW.meta).versionId IS NULL THEN
                RAISE EXCEPTION '% field in meta is not nullable', field_name;
            END IF;

        ELSEIF field_name = 'lastUpdated' THEN
            IF (NEW.meta).lastUpdated IS NULL THEN
                RAISE EXCEPTION '% field in meta is not nullable', field_name;
            END IF;

        ELSEIF field_name = 'profile' THEN
            IF (NEW.meta).profile IS NULL THEN
                RAISE EXCEPTION '% field in meta is not nullable', field_name;
            END IF;

        ELSEIF field_name = 'security' THEN
            IF (NEW.meta).security IS NULL THEN
                RAISE EXCEPTION '% field in meta is not nullable', field_name;
            END IF;

        ELSEIF field_name = 'tag' THEN
            IF (NEW.meta).tag IS NULL THEN
                RAISE EXCEPTION '% field in meta is not nullable', field_name;
            END IF;
        END IF;

        RETURN NEW;
    END;
$validate_meta_fields$ LANGUAGE plpgsql;


CREATE TRIGGER validate_meta_fields BEFORE INSERT OR UPDATE ON "Organization"
    FOR EACH ROW EXECUTE PROCEDURE validate_meta_fields(constraints);
