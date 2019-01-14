import pytest

from sqlalchemy import Column
from sqlalchemy_utils import register_composites
from sqlalchemy.exc import StatementError

from fhir_server.elements import primitives
from fhir_server.elements.complex.annotation import (
    AnnotationField,
    Annotation as AnnotationDef,
)


class TestAnnotation(object):
    @pytest.fixture
    def TestAnnotationModel(self, Base):
        class TestAnnotationModel(Base):
            __tablename__ = "test_annotation"
            id = Column(primitives.IntegerField, primary_key=True)
            annotation = Column(AnnotationField())

        return TestAnnotationModel

    def test_post_data(self, session, TestAnnotationModel):
        post = TestAnnotationModel(
            id=1,
            annotation={
                "authorString": "author string",
                "text": "text",
                "time": "2011-05-24",
                "authorReference": {
                    "reference": "reference url",
                    "display": "Patient X",
                },
            },
        )

        session.execute(
            """
            CREATE TABLE test_annotation (
                id INTEGER, annotation fhir_annotation);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestAnnotationModel).first()
        assert get.id == 1
        assert get.annotation.authorReference.display == "Patient X"

    @pytest.fixture
    def ProfiledAnnotation(self):
        class Annotation(AnnotationDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    if field.name == "authorString":
                        field.cardinality["mini"] = 1
                    if field.name == "time":
                        field.cardinality["mini"] = 1
                    if field.name == "authorReference":
                        field.cardinality["mini"] = 1
                return fields

        return Annotation()()

    @pytest.fixture
    def TestProfiledAnnotation(self, Base):
        class TestProfiledAnnotation(Base):
            __tablename__ = "test_annotation"
            id = Column(primitives.IntegerField, primary_key=True)
            annotation = Column(self.ProfiledAnnotation())

        return TestProfiledAnnotation

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledAnnotation()
        authorString = [
            field for field in fields.columns if field.name == "authorString"
        ]
        time = [field for field in fields.columns if field.name == "time"]
        authorReference = [
            field for field in fields.columns if (field.name == "authorReference")
        ]

        assert not authorString[0].nullable
        assert not time[0].nullable
        assert not authorReference[0].nullable

    def test_post_data_field_city_present(self, session, TestProfiledAnnotation):
        post = TestProfiledAnnotation(
            id=1,
            annotation={
                "authorString": "author string",
                "text": "text",
                "time": "2011-05-24",
                "authorReference": {
                    "reference": "reference url",
                    "display": "Patient X",
                },
            },
        )

        session.execute(
            """
            CREATE TABLE test_annotation (
                id INTEGER, annotation fhir_annotation);"""
        )

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledAnnotation).first()
        assert get.id == 1
        assert get.annotation.authorString == "author string"

    def test_fail_to_post_data_missing_city(self, session, TestProfiledAnnotation):
        post = TestProfiledAnnotation(
            id=1,
            annotation={
                "authorReference": {
                    "reference": "reference url",
                    "display": "Patient X",
                }
            },
        )

        session.execute(
            """
            CREATE TABLE test_annotation (
                id INTEGER, annotation fhir_annotation);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ("Field authorString in column fhir_annotation not " "nullable") in str(
            excinfo.value
        )
        assert ("Field time in column fhir_annotation not " "nullable") in str(
            excinfo.value
        )
        assert ("Field text in column fhir_annotation not " "nullable") in str(
            excinfo.value
        )

    def test_fail_to_post_data_missing_authorReference(
        self, session, TestProfiledAnnotation
    ):
        post = TestProfiledAnnotation(
            id=1,
            annotation={
                "authorString": "author string",
                "text": "text",
                "time": "2011-05-24",
            },
        )

        session.execute(
            """
            CREATE TABLE test_annotation (
                id INTEGER, annotation fhir_annotation);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert (
            "Field authorReference in column fhir_annotation not " "nullable"
        ) in str(excinfo.value)
