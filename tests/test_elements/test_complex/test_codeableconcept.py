import pytest

from sqlalchemy import Column
from sqlalchemy_utils import register_composites
from sqlalchemy.exc import StatementError

from fhir_server.elements import primitives
from fhir_server.elements.complex.codeableconcept import (
    CodeableConceptField,
    CodeableConcept as CodeableConceptDef,
)


class TestCodeableConcept(object):
    @pytest.fixture
    def TestCodeableConceptModel(self, Base):
        class TestCodeableConceptModel(Base):
            __tablename__ = "test_codeable_concept"
            id = Column(primitives.IntegerField, primary_key=True)
            codeable_concept = Column(CodeableConceptField())

        return TestCodeableConceptModel

    def test_post_data(self, session, TestCodeableConceptModel):
        post = TestCodeableConceptModel(
            id=1,
            codeable_concept={
                "text": "text",
                "coding": [
                    {
                        "code": "dkls323-3223hj",
                        "display": "display",
                        "system": "http://testing.test.com",
                        "userSelected": True,
                        "version": "2.3",
                    },
                    {
                        "code": "dkls323-3223hj",
                        "display": "display",
                        "system": "http://testing.test.com",
                        "userSelected": True,
                        "version": "2.3",
                    },
                ],
            },
        )

        session.execute(
            """
            CREATE TABLE test_codeable_concept (
                id INTEGER, codeable_concept fhir_codeableconcept);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestCodeableConceptModel).first()
        assert get.id == 1
        assert get.codeable_concept.coding[0].version == "2.3"

    def test_post_data_with_null_coding_field(self, session, TestCodeableConceptModel):
        post = TestCodeableConceptModel(id=1, codeable_concept={"text": "text"})

        session.execute(
            """
            CREATE TABLE test_codeable_concept (
                id INTEGER, codeable_concept fhir_codeableconcept);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestCodeableConceptModel).first()
        assert get.id == 1
        assert get.codeable_concept.coding is None

    @pytest.fixture
    def ProfiledCodeableConcept(self):
        class CodeableConcept(CodeableConceptDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality["mini"] = 1

                return fields

        return CodeableConcept()()

    @pytest.fixture
    def TestProfiledCodeableConcept(self, Base):
        class TestProfiledCodeableConcept(Base):
            __tablename__ = "test_codeable_concept"
            id = Column(primitives.IntegerField, primary_key=True)
            codeable_concept = Column(self.ProfiledCodeableConcept())

        return TestProfiledCodeableConcept

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledCodeableConcept()
        text = [field for field in fields.columns if field.name == "text"]
        coding = [field for field in fields.columns if field.name == "coding"]

        assert not text[0].nullable
        assert not coding[0].nullable

    def test_post_data_fields_present(self, session, TestProfiledCodeableConcept):
        post = TestProfiledCodeableConcept(
            id=1,
            codeable_concept={
                "text": "text",
                "coding": [
                    {
                        "code": "dkls323-3223hj",
                        "display": "display",
                        "system": "http://testing.test.com",
                        "userSelected": True,
                        "version": "2.3",
                    },
                    {
                        "code": "dkls323-3223hj",
                        "display": "display",
                        "system": "http://testing.test.com",
                        "userSelected": True,
                        "version": "2.3",
                    },
                ],
            },
        )

        session.execute(
            """
            CREATE TABLE test_codeable_concept (
                id INTEGER, codeable_concept fhir_codeableconcept);"""
        )

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledCodeableConcept).first()
        assert get.id == 1
        assert get.codeable_concept.coding[0].display == "display"

    def test_fail_to_post_data_missing_fields(
        self, session, TestProfiledCodeableConcept
    ):
        post = TestProfiledCodeableConcept(id=1, codeable_concept={})

        session.execute(
            """
            CREATE TABLE test_codeable_concept (
                id INTEGER, codeable_concept fhir_codeableconcept);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ("Field text in column fhir_codeableconcept not " "nullable") in str(
            excinfo.value
        )
        assert ("Field coding in column fhir_codeableconcept not " "nullable") in str(
            excinfo.value
        )
