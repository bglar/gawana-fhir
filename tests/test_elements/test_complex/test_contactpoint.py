import pytest

from unittest.mock import patch

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.contactpoint import (
    ContactPointField,
    ContactPoint as ContactPointDef,
)


class TestContactPoint(object):
    @pytest.fixture
    def TestContactPointModel(self, Base):
        class TestContactPointModel(Base):
            __tablename__ = "test_contactpoint"
            id = Column(primitives.IntegerField, primary_key=True)
            contactpoint = Column(ContactPointField())

        return TestContactPointModel

    @patch("fhir_server.helpers.validations.requests.get")
    def test_post_data(self, mock_get, session, TestContactPointModel):
        mock_get.return_value.json.return_value = {
            "count": 2,
            "data": [{"code": "phone"}, {"code": "home"}],
        }
        post = TestContactPointModel(
            id=1,
            contactpoint={
                "rank": 2,
                "system": "phone",
                "use": "home",
                "value": "+254712122988",
                "period": {"start": "2011-05-24", "end": "2011-06-24"},
            },
        )

        session.execute(
            """
            CREATE TABLE test_contactpoint (
                id INTEGER, contactpoint fhir_contactpoint);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestContactPointModel).first()
        assert get.id == 1
        assert get.contactpoint.value == "+254712122988"

    @patch("fhir_server.helpers.validations.requests.get")
    def test_post_data_with_system_not_defined_in_valueset(
        self, mock_get, session, TestContactPointModel
    ):
        mock_get.return_value.json.return_value = {
            "count": 2,
            "data": [{"code": "work"}],
        }
        post = TestContactPointModel(
            id=1,
            contactpoint={
                "rank": 2,
                "system": "sytem",
                "use": "work",
                "value": "+254712122988",
                "period": {"start": "2011-05-24", "end": "2011-06-24"},
            },
        )

        session.execute(
            """
            CREATE TABLE test_contactpoint (
                id INTEGER, contactpoint fhir_contactpoint);"""
        )

        session.add(post)

        register_composites(session.connection())
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert "The contactpoint system must be defined in" in str(excinfo.value)

    @patch("fhir_server.helpers.validations.requests.get")
    def test_post_data_with_use_not_defined_in_valueset(
        self, mock_get, session, TestContactPointModel
    ):
        mock_get.return_value.json.return_value = {
            "count": 2,
            "data": [{"code": "phone"}],
        }
        post = TestContactPointModel(
            id=1,
            contactpoint={
                "rank": 2,
                "system": "phone",
                "use": "nothere",
                "value": "+254712122988",
                "period": {"start": "2011-05-24", "end": "2011-06-24"},
            },
        )

        session.execute(
            """
            CREATE TABLE test_contactpoint (
                id INTEGER, contactpoint fhir_contactpoint);"""
        )

        session.add(post)

        register_composites(session.connection())
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert "The contactpoint use must be defined in" in str(excinfo.value)

    def test_post_data_with_null_contactpoint_field(
        self, session, TestContactPointModel
    ):
        post = TestContactPointModel(id=1, contactpoint={})

        session.execute(
            """
            CREATE TABLE test_contactpoint (
                id INTEGER, contactpoint fhir_contactpoint);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestContactPointModel).first()
        assert get.id == 1
        assert get.contactpoint.rank is None

    @pytest.fixture
    def ProfiledContactPoint(self):
        class ContactPoint(ContactPointDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality["mini"] = 1

                return fields

        return ContactPoint()()

    @pytest.fixture
    def TestProfiledContactPoint(self, Base):
        class TestProfiledContactPoint(Base):
            __tablename__ = "test_contactpoint"
            id = Column(primitives.IntegerField, primary_key=True)
            contactpoint = Column(self.ProfiledContactPoint())

        return TestProfiledContactPoint

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledContactPoint()
        rank = [field for field in fields.columns if field.name == "rank"]
        system = [field for field in fields.columns if field.name == "system"]
        use = [field for field in fields.columns if field.name == "use"]
        value = [field for field in fields.columns if field.name == "value"]
        period = [field for field in fields.columns if field.name == "period"]

        assert not rank[0].nullable
        assert not system[0].nullable
        assert not use[0].nullable
        assert not value[0].nullable
        assert not period[0].nullable

    @patch("fhir_server.helpers.validations.requests.get")
    def test_post_data_fields_present(
        self, mock_get, session, TestProfiledContactPoint
    ):
        mock_get.return_value.json.return_value = {
            "count": 2,
            "data": [{"code": "phone"}, {"code": "work"}],
        }
        post = TestProfiledContactPoint(
            id=1,
            contactpoint={
                "rank": 2,
                "system": "phone",
                "use": "work",
                "value": "+254712122988",
                "period": {"start": "2011-05-24", "end": "2011-06-24"},
            },
        )

        session.execute(
            """
            CREATE TABLE test_contactpoint (
                id INTEGER, contactpoint fhir_contactpoint);"""
        )

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledContactPoint).first()
        assert get.id == 1
        assert get.contactpoint.rank == 2

    def test_fail_to_post_data_missing_fields(self, session, TestProfiledContactPoint):
        post = TestProfiledContactPoint(id=1, contactpoint={})

        session.execute(
            """
            CREATE TABLE test_contactpoint (
                id INTEGER, contactpoint fhir_contactpoint);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ("Field rank in column fhir_contactpoint not " "nullable") in str(
            excinfo.value
        )
        assert ("Field system in column fhir_contactpoint not " "nullable") in str(
            excinfo.value
        )
        assert ("Field use in column fhir_contactpoint not " "nullable") in str(
            excinfo.value
        )
        assert ("Field value in column fhir_contactpoint not " "nullable") in str(
            excinfo.value
        )
        assert ("Field period in column fhir_contactpoint not " "nullable") in str(
            excinfo.value
        )
