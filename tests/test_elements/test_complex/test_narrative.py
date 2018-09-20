import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites
from fhir_server.elements import primitives
from fhir_server.elements.complex.narrative import NarrativeField


class TestNarrative(object):

    @pytest.fixture
    def TestNarrativeModel(self, Base):
        class TestNarrativeModel(Base):
            __tablename__ = 'test_narrative'
            id = Column(primitives.IntegerField, primary_key=True)
            narrative = Column(NarrativeField())
        return TestNarrativeModel

    def test_post_data(self, session, TestNarrativeModel):
        post = TestNarrativeModel(
            id=1,
            narrative={
                'div': '<a style=someattribute>someattribute</a><b>strong</b>',
                'status': 'generated'
            }
        )

        session.execute("""
            CREATE TABLE test_narrative (
                id INTEGER, narrative fhir_narrative);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestNarrativeModel).first()
        assert get.id == 1
        assert get.narrative.status == 'generated'

    def test_reject_data_with_invalid_tags(
            self, session, TestNarrativeModel):
        post = TestNarrativeModel(
            id=1,
            narrative={
                'div': '<lala>sometag</lala><b>strong</b>',
                'status': 'generated'
            }
        )

        session.execute("""
            CREATE TABLE test_narrative (
                id INTEGER, narrative fhir_narrative);""")

        session.add(post)

        register_composites(session.connection())

        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'The tag lala is not valid' in str(excinfo.value)

    def test_reject_data_with_invalid_attributes(
            self, session, TestNarrativeModel):
        post = TestNarrativeModel(
            id=1,
            narrative={
                'div': '<a noattr=someattribute></a><b>strong</b>',
                'status': 'generated'
            }
        )

        session.execute("""
            CREATE TABLE test_narrative (
                id INTEGER, narrative fhir_narrative);""")

        session.add(post)

        register_composites(session.connection())

        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'The attribute noattr is not valid in' in str(excinfo.value)

    def test_reject_data_with_status_not_in_valuesets(
            self, session, TestNarrativeModel):
        post = TestNarrativeModel(
            id=1,
            narrative={
                'div': '<a>someattribute</a><b>strong</b>',
                'status': 'status'
            }
        )

        session.execute("""
            CREATE TABLE test_narrative (
                id INTEGER, narrative fhir_narrative);""")

        session.add(post)

        register_composites(session.connection())

        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'The narrative status must be defined in' in str(excinfo.value)

    def test_reject_content_containing_empty_string(
            self, session, TestNarrativeModel):
        post = TestNarrativeModel(
            id=1,
            narrative={
                'div': ' ',
                'status': 'generated'
            }
        )

        session.execute("""
            CREATE TABLE test_narrative (
                id INTEGER, narrative fhir_narrative);""")

        session.add(post)

        register_composites(session.connection())

        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'narrative content must not be an empty string' in str(
            excinfo.value)
