from jsonschema import validate

import json
from sqlalchemy.dialects import postgresql
from sqlalchemy import TypeDecorator


class OpenType(TypeDecorator):

    """
    Create a json field to accommodate allowable types
    ------------------------------------------------------------------
    {
        "valueString": "values",
        "valueInt": "values",
        "valueOID": "values",
        "valueDatetime": "values"
    }
    OR for nested extensions
    [
        {
            "valueString": "values",
            "valueInt": "values",
        },
        {
            "valueOID": "values",
            "valueDatetime": "values"
        }
    ]
    ------------------------------------------------------------------
    The json field should verify that only a list of the allowable types
    is supplied and reject garbage.
    Add validations to each entry / validates entries
    """

    impl = postgresql.JSONB

    def coerce_compared_value(self, op, value):
        return self.impl.coerce_compared_value(op, value)

    def process_bind_param(self, value, dialect):
        """
        The schema variable defined here is used to constrain the field names
        and also naively constrain the data types. Notice that the data types
        in this server go beyond the schema definition. Example: Here uri is
        defined as a string field but the server validates this as a URI field.
        (jsonschema)[https://pypi.python.org/pypi/jsonschema] is used.

        :param value:
        :param dialect:
        :return: valid value:
        """
        schema = {
            "description": "schema validating extensions type in FHIR",
            "definition1": {
                "valueX": {
                    "type": "object",
                    "properties": {
                        "valueBoolean": {"type": "boolean"},
                        "valueInteger": {"type": "integer"},
                        "valueDecimal": {"type": "integer"},
                        "valueBase64Binary": {"type": "string"},
                        "valueInstant": {"type": "string"},
                        "valueString": {"type": "string"},
                        "valueUri": {"type": "string"},
                        "valueDate": {"type": "string"},
                        "valueDateTime": {"type": "string"},
                        "valueTime": {"type": "string"},
                        "valueCode": {"type": "string"},
                        "valueOid": {"type": "string"},
                        "valueId": {"type": "string"},
                        "valueUnsignedInt": {"type": "integer"},
                        "valuePositiveInt": {"type": "integer"},
                        "valueMarkdown": {"type": "string"},
                        "valueAnnotation": {"type": "object"},
                        "valueAttachment": {"type": "object"},
                        "valueIdentifier": {"type": "object"},
                        "valueCodeableConcept": {"type": "object"},
                        "valueCoding": {"type": "object"},
                        "valueQuantity": {"type": "object"},
                        "valueRange": {"type": "object"},
                        "valuePeriod": {"type": "object"},
                        "valueRatio": {"type": "object"},
                        "valueSampledData": {"type": "object"},
                        "valueSignature": {"type": "object"},
                        "valueHumanName": {"type": "object"},
                        "valueAddress": {"type": "object"},
                        "valueContactPoint": {"type": "object"},
                        "valueTiming": {"type": "object"},
                        "valueReference": {"type": "object"},
                        "valueMeta": {"type": "object"}
                    },
                    "additionalProperties": False
                },
            },

            "definition2": {
                "nestedExtension": {
                    "type": "object",
                    "properties": {
                        "url": {"type", "string"},
                        "extension": {"type": "array"}
                    },
                    "required": ["url"],
                    "additionalProperties": False
                }
            },

            "oneOf": [
                {"$ref": "#definition1/valueX"},
                {"$ref": "#definition2/nestedExtension"},
            ]
        }

        if value is not None:
            if not isinstance(value, str):
                try:
                    validate(value, schema)
                except Exception:
                    raise ValueError(
                        "The data provided for the extensions field is invalid")

            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
