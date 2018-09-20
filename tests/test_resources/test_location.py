import pytest
from sqlalchemy_utils import register_composites

from fhir_server.resources.identification.location import Location


class TestLocation(object):
    id = "1"
    implicitRules = "https://gawana-fhir.constraints.co.ke/rules"
    language = "EN"
    identifier = [{
        "system": "system",
        "use": "secondary",
        "value": "value111",
        "assigner": {
            "reference": "reference url",
            "display": "Patient X"
        },
        "type": {
            "text": "text",
            "coding": [
                {
                    "code": "UDI",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3"
                }]
        },
        "period": {
            "start": "2011-05-24",
            "end": "2011-06-24"
        }
    }]
    status = "suspended"
    name = "Nairobi"
    description = "This is a Community based organization"
    mode = "instance"
    locationType = {
        "text": "text",
        "coding": [
            {
                "code": "FM",
                "display": "display",
                "system": "http://testing.test.com",
                "userSelected": "True",
                "version": "2.3"
            }]
    }
    telecom = [{
        "rank": 2,
        "system": "phone",
        "use": "work",
        "value": "+254712122988",
        "period": {
            "start": "2011-05-24",
            "end": "2011-06-24"
        }
    }]
    address = [{
        "use": "work",
        "text": "text",
        "type": "postal",
        "state": "state",
        "postal_code": "postal code",
        "line": ["line1", "line2"],
        "district": "district",
        "country": "KEN",
        "city": "city",
        "period": {
            "start": "2011-05-24",
            "end": "2011-06-24"
        }
    }]
    physical_type = {
        "text": "text",
        "coding": [
            {
                "code": "area",
                "display": "display",
                "system": "http://testing.test.com",
                "userSelected": "True",
                "version": "2.3"
            }]
    }
    position = {
        "longitude": 12.3323323,
        "latitude": 32.3232324,
        "altitude": 0.24242424
    }
    managingOrganization = {
        "display": "display",
        "reference": "http://spark.furore.com/fhir/Organization/1"
    }
    part_of = {
        "display": "display",
        "reference": "http://spark.furore.com/fhir/Location/2"
    }

    def test_location_repr(self):
        data = Location(
            id=self.id,
            implicitRules=self.implicitRules,
            language=self.language,
            identifier=self.identifier,
            status=self.status,
            name=self.name,
            description=self.description,
            mode=self.mode,
            type=self.locationType,
            telecom=self.telecom,
            address=self.address,
            physicalType=self.physical_type,
            position=self.position,
            managingOrganization=self.managingOrganization,
            partOf=self.part_of
        )

        assert str(data) == "<Location 'Nairobi'>"

    def test_code_fields_validator_none_value(self):
        data = Location(
            id=self.id,
            implicitRules=self.implicitRules,
            language=self.language,
            identifier=self.identifier,
            status=self.status,
            name=self.name,
            description=self.description,
            mode=self.mode,
            type=self.locationType,
            telecom=self.telecom,
            address=self.address,
            physicalType=None,
            position=self.position,
            managingOrganization=self.managingOrganization,
            partOf=self.part_of
        )

        assert str(data) == "<Location 'Nairobi'>"

    def test_save_location(self, session):
        data = Location(
            id=self.id,
            implicitRules=self.implicitRules,
            language=self.language,
            identifier=self.identifier,
            status=self.status,
            name=self.name,
            description=self.description,
            mode=self.mode,
            type=self.locationType,
            telecom=self.telecom,
            address=self.address,
            physicalType=self.physical_type,
            position=self.position,
            managingOrganization=self.managingOrganization,
            partOf=self.part_of
        )
        session.add(data)
        session.commit()
        register_composites(session.connection())
        get = session.query(Location).first()
        assert get.id == '1'
        assert get.language == 'EN'

    def test_reject_data_if_status_is_not_valid(self):
        with pytest.raises(TypeError) as excinfo:
            Location(
                id=self.id,
                implicitRules=self.implicitRules,
                language=self.language,
                identifier=self.identifier,
                status='invalid',
                name=self.name,
                description=self.description,
                mode=self.mode,
                type=self.locationType,
                telecom=self.telecom,
                address=self.address,
                physicalType=self.physical_type,
                position=self.position,
                managingOrganization=self.managingOrganization,
                partOf=self.part_of
            )
        assert "The location status must be defined in" in str(excinfo.value)

    def test_reject_data_if_mode_is_not_valid(self):
        with pytest.raises(TypeError) as excinfo:
            Location(
                id=self.id,
                implicitRules=self.implicitRules,
                language=self.language,
                identifier=self.identifier,
                status=self.status,
                name=self.name,
                description=self.description,
                mode='invalid',
                type=self.locationType,
                telecom=self.telecom,
                address=self.address,
                physicalType=self.physical_type,
                position=self.position,
                managingOrganization=self.managingOrganization,
                partOf=self.part_of
            )
        assert "The location mode must be defined in" in str(excinfo.value)

    def test_reject_data_if_locationType_is_not_valid(self):
        with pytest.raises(TypeError) as excinfo:
            Location(
                id=self.id,
                implicitRules=self.implicitRules,
                language=self.language,
                identifier=self.identifier,
                status=self.status,
                name=self.name,
                description=self.description,
                mode=self.mode,
                type={
                    "text": "text",
                    "coding": [
                        {
                            "code": "invalid",
                            "display": "display",
                            "system": "http://testing.test.com",
                            "userSelected": "True",
                            "version": "2.3"
                        }]
                },
                telecom=self.telecom,
                address=self.address,
                physicalType=self.physical_type,
                position=self.position,
                managingOrganization=self.managingOrganization,
                partOf=self.part_of
            )
        assert "The location type code must be defined in" in str(excinfo.value)

    def test_reject_data_if_physical_type_is_not_valid(self):
        with pytest.raises(TypeError) as excinfo:
            Location(
                id=self.id,
                implicitRules=self.implicitRules,
                language=self.language,
                identifier=self.identifier,
                status=self.status,
                name=self.name,
                description=self.description,
                mode=self.mode,
                type=self.locationType,
                telecom=self.telecom,
                address=self.address,
                physicalType={
                    "text": "text",
                    "coding": [
                        {
                            "code": "invalid",
                            "display": "display",
                            "system": "http://testing.test.com",
                            "userSelected": "True",
                            "version": "2.3"
                        }]
                },
                position=self.position,
                managingOrganization=self.managingOrganization,
                partOf=self.part_of
            )
        assert "The location physical type code must be defined in" in str(
            excinfo.value)
