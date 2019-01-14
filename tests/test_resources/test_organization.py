from unittest.mock import patch

import pytest
from sqlalchemy_utils import register_composites

from fhir_server.resources.identification.organization import Organization


class TestOrganization(object):
    valuesets_data = [
        {"code": "secondary"},
        {"code": "UDI"},
        {"code": "prov"},
        {"code": "dkls323-3223hj"},
        {"code": "work"},
        {"code": "phone"},
        {"code": "generated"},
    ]
    id = "109"
    implicitRules = "https://gawana-fhir.constraints.co.ke/rules"
    language = "EN"
    active = True
    name = "Test Organization"
    identifier = [
        {
            "system": "system",
            "use": "secondary",
            "value": "value111",
            "assigner": {"reference": "reference url", "display": "Patient X"},
            "type": {
                "text": "text",
                "coding": [
                    {
                        "code": "UDI",
                        "display": "display",
                        "system": "http://testing.test.com",
                        "userSelected": "True",
                        "version": "2.3",
                    }
                ],
            },
            "period": {"start": "2011-05-24", "end": "2011-06-24"},
        }
    ]
    org_type = {
        "text": "text",
        "coding": [
            {
                "code": "prov",
                "display": "display",
                "system": "http://testing.test.com",
                "userSelected": "True",
                "version": "2.3",
            }
        ],
    }
    telecom = [
        {
            "rank": 2,
            "system": "phone",
            "use": "work",
            "value": "+254712122988",
            "period": {"start": "2011-05-24", "end": "2011-06-24"},
        }
    ]
    address = [
        {
            "use": "work",
            "text": "text",
            "type": "postal",
            "state": "state",
            "postal_code": "postal code",
            "line": ["line1", "line2"],
            "district": "district",
            "country": "KEN",
            "city": "city",
            "period": {"start": "2011-05-24", "end": "2011-06-24"},
        }
    ]
    partOf = {
        "display": "display",
        "reference": "http://spark.furore.com/fhir/Organization/1",
    }
    contact = [{}]
    meta = {
        "versionId": "1.2a23",
        "lastUpdated": "2011-05-24T10:10:10+0300",
        "profile": [
            "http://example.com/fhir/Patient/",
            "http://example.com/fhir/Organization/",
        ],
        "security": [
            {
                "code": "dkls323-3223hj",
                "display": "display",
                "system": "http://example.com/fhir/Security/",
                "userSelected": "True",
                "version": "2.3",
            }
        ],
        "tag": [
            {
                "code": "dkls323-3223hj",
                "display": "display",
                "system": "http://example.com/fhir/tag/",
                "userSelected": "True",
                "version": "2.3",
            }
        ],
    }

    @patch("fhir_server.helpers.validations.requests.get")
    def test_organization_repr(self, mock_get):
        mock_get.return_value.json.return_value = {
            "count": len(self.valuesets_data),
            "data": self.valuesets_data,
        }
        data = Organization(
            id=self.id,
            implicitRules=self.implicitRules,
            language=self.language,
            active=self.active,
            name=self.name,
            identifier=self.identifier,
            type=self.org_type,
            telecom=self.telecom,
            address=self.address,
            partOf=self.partOf,
            contact=self.contact,
            meta=self.meta,
        )

        assert str(data) == "<'Organization' 'Test Organization'>"

    @patch("fhir_server.elements.base.reference_validator.reference_resolution")
    @patch("fhir_server.helpers.validations.requests.get")
    def test_save_organization(self, mock_get, mock_ref, session):
        mock_ref.return_value = True
        mock_get.return_value.json.return_value = {
            "count": len(self.valuesets_data),
            "data": self.valuesets_data,
        }
        data = Organization(
            id=self.id,
            implicitRules=self.implicitRules,
            language=self.language,
            active=self.active,
            name=self.name,
            identifier=self.identifier,
            type=self.org_type,
            telecom=self.telecom,
            address=None,
            partOf=self.partOf,
            contact=self.contact,
            meta=self.meta,
        )
        session.add(data)
        session.commit()
        register_composites(session.connection())
        get = session.query(Organization).first()
        assert get.name == "Test Organization"

    @patch("fhir_server.helpers.validations.requests.get")
    def test_reject_data_if_org_type_not_in_valuesets(self, mock_get, session):
        mock_get.return_value.json.return_value = {
            "count": len(self.valuesets_data),
            "data": self.valuesets_data,
        }
        with pytest.raises(TypeError) as excinfo:
            Organization(
                id=self.id,
                implicitRules=self.implicitRules,
                language=self.language,
                active=self.active,
                name=self.name,
                identifier=self.identifier,
                type={
                    "text": "text",
                    "coding": [
                        {
                            "code": "notorgtype",
                            "display": "display",
                            "system": "http://testing.test.com",
                            "userSelected": "True",
                            "version": "2.3",
                        }
                    ],
                },
                telecom=self.telecom,
                address=self.address,
                partOf=self.partOf,
                contact=self.contact,
                meta=self.meta,
            )
        assert "The organization type code must be defined in" in str(excinfo.value)

    @patch("fhir_server.helpers.validations.requests.get")
    def test_reject_data_if_address_is_of_use_home(self, mock_get):
        mock_get.return_value.json.return_value = {
            "count": len(self.valuesets_data),
            "data": self.valuesets_data,
        }
        with pytest.raises(ValueError) as excinfo:
            Organization(
                id=self.id,
                implicitRules=self.implicitRules,
                language=self.language,
                active=self.active,
                name=self.name,
                identifier=self.identifier,
                type=self.org_type,
                telecom=self.telecom,
                address=[
                    {
                        "use": "home",
                        "text": "text",
                        "type": "postal",
                        "state": "state",
                        "postal_code": "postal code",
                        "line": ["line1", "line2"],
                        "district": "district",
                        "country": "KEN",
                        "city": "city",
                        "period": {"start": "2011-05-24", "end": "2011-06-24"},
                    }
                ],
                partOf=self.partOf,
                contact=self.contact,
                meta=self.meta,
            )
        assert "An address of an organization can never be of " "use `home`" in str(
            excinfo.value
        )

    @patch("fhir_server.helpers.validations.requests.get")
    def test_reject_data_if_telecom_is_of_use_home(self, mock_get):
        mock_get.return_value.json.return_value = {
            "count": len(self.valuesets_data),
            "data": self.valuesets_data,
        }
        with pytest.raises(ValueError) as excinfo:
            Organization(
                id=self.id,
                implicitRules=self.implicitRules,
                language=self.language,
                active=self.active,
                name=self.name,
                identifier=self.identifier,
                type=self.org_type,
                telecom=[
                    {
                        "rank": "2",
                        "system": "phone",
                        "use": "home",
                        "value": "+254712122988",
                        "period": {"start": "2011-05-24", "end": "2011-06-24"},
                    }
                ],
                address=self.address,
                partOf=self.partOf,
                contact=self.contact,
                meta=self.meta,
            )
        assert "The telecom of an organization can never be of " "use `home`" in str(
            excinfo.value
        )

    @patch("fhir_server.helpers.validations.requests.get")
    def test_reject_data_if_partOf_reference_is_not_valid(self, mock_get):
        mock_get.return_value.json.return_value = {
            "count": len(self.valuesets_data),
            "data": self.valuesets_data,
        }
        with pytest.raises(ValueError) as excinfo:
            Organization(
                id=self.id,
                implicitRules=self.implicitRules,
                language=self.language,
                active=self.active,
                name=self.name,
                identifier=self.identifier,
                type=self.org_type,
                address=self.address,
                partOf={
                    "display": "display",
                    "reference": "http://spark.furore.com/fhir/Patient/1",
                },
                contact=self.contact,
                meta=self.meta,
            )
        assert "The resource reference is not valid" in str(excinfo.value)
