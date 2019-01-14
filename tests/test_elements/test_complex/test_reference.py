from unittest.mock import patch

import pytest

from flask import Response
from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.reference import (
    ReferenceField,
    Reference as ReferenceDef,
)


class TestReference(object):
    @pytest.fixture
    def TestReferenceModel(self, Base):
        class TestReferenceModel(Base):
            __tablename__ = "test_reference"
            id = Column(primitives.IntegerField, primary_key=True)
            reference = Column(ReferenceField())

        return TestReferenceModel

    @patch("fhir_server.elements.base.reference_validator.requests.get")
    def test_post_data_with_external_reference(
        self, mock_get, session, TestReferenceModel
    ):
        mock_get.return_value = Response(status=200)
        post = TestReferenceModel(
            id=1,
            reference={
                "display": "display",
                "reference": "http://spark.furore.com/fhir/Patient/89/"
                "_history/spark45",
            },
        )

        session.execute(
            """
            CREATE TABLE test_reference (
                id INTEGER, reference fhir_reference);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestReferenceModel).first()
        assert get.id == 1
        assert get.reference.display == "display"

    def test_reject_data_with_invalid_external_reference(
        self, session, TestReferenceModel
    ):
        post = TestReferenceModel(
            id=1,
            reference={
                "display": "display",
                "reference": "http://not.furore.com/fhir/Patient/89/",
            },
        )

        session.execute(
            """
            CREATE TABLE test_reference (
                id INTEGER, reference fhir_reference);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert "The reference provided is not valid." in str(excinfo.value)

    def test_reject_data_with_invalid_internal_reference(
        self, session, TestReferenceModel
    ):
        post = TestReferenceModel(
            id=1, reference={"display": "display", "reference": "Patient/89"}
        )

        session.execute(
            """
            CREATE TABLE test_reference (
                id INTEGER, reference fhir_reference);"""
        )

        session.add(post)
        # with pytest.raises(StatementError) as excinfo:
        session.commit()
        # assert '(requests.exceptions.ConnectionError)' in str(excinfo.value)

    def test_reject_post_data_with_invalid_external_reference(
        self, session, TestReferenceModel
    ):
        post = TestReferenceModel(
            id=1,
            reference={
                "display": "display",
                "reference": "http://spark.furore.com/fhir/Patient/001/"
                "_history/spark45",
            },
        )

        session.execute(
            """
            CREATE TABLE test_reference (
                id INTEGER, reference fhir_reference);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert "We were unable to resolve a resource reference at" in str(excinfo.value)

    def test_post_data_with_null_reference_field(self, session, TestReferenceModel):
        post = TestReferenceModel(id=1, reference={})

        session.execute(
            """
            CREATE TABLE test_reference (
                id INTEGER, reference fhir_reference);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestReferenceModel).first()
        assert get.id == 1
        assert get.reference.display is None

    @pytest.fixture
    def ProfiledReference(self):
        class Reference(ReferenceDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality["mini"] = 1

                return fields

        return Reference()()

    @pytest.fixture
    def TestProfiledReference(self, Base):
        class TestProfiledReference(Base):
            __tablename__ = "test_reference"
            id = Column(primitives.IntegerField, primary_key=True)
            reference = Column(self.ProfiledReference())

        return TestProfiledReference

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledReference()
        display = [field for field in fields.columns if field.name == "display"]
        reference = [field for field in fields.columns if field.name == "reference"]

        assert not display[0].nullable
        assert not reference[0].nullable

    @patch("fhir_server.elements.base.reference_validator.requests.get")
    def test_post_data_fields_present(self, mock_get, session, TestProfiledReference):

        mock_get.return_value = Response(status=200)

        post = TestProfiledReference(
            id=1,
            reference={
                "display": "display",
                "reference": "http://spark.furore.com/fhir/Patient/89/"
                "_history/spark45",
            },
        )

        session.execute(
            """
            CREATE TABLE test_reference (
                id INTEGER, reference fhir_reference);"""
        )

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledReference).first()
        assert get.id == 1
        assert get.reference.display == "display"

    def test_fail_to_post_data_missing_fields(self, session, TestProfiledReference):
        post = TestProfiledReference(id=1, reference={})

        session.execute(
            """
            CREATE TABLE test_reference (
                id INTEGER, reference fhir_reference);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ("Field reference in column fhir_reference not " "nullable") in str(
            excinfo.value
        )
        assert ("Field display in column fhir_reference not " "nullable") in str(
            excinfo.value
        )
