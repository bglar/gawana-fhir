import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.age import (
    Age as AgeDef, AgeField)


class TestAge(object):

    @pytest.fixture
    def TestAgeModel(self, Base):
        class TestAgeModel(Base):
            __tablename__ = 'test_age'
            id = Column(primitives.IntegerField, primary_key=True)
            age = Column(AgeField())
        return TestAgeModel

    def test_post_data(self, session, TestAgeModel):
        post = TestAgeModel(
            id=1,
            age={
                'code': 'mo',
                'system': 'http://unitsofmeasure.org',
                'unit': 'mo',
                'value': 24,
                'comparator': '<'
            }
        )

        session.execute("""
            CREATE TABLE test_age (
                id INTEGER, age fhir_age);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestAgeModel).first()
        assert get.id == 1
        assert get.age.value == 24

    def test_reject_posting_data_with_code_not_in_valueset(
            self, session, TestAgeModel):
        post = TestAgeModel(
            id=1,
            age={
                'code': 'notinvalueset',
                'system': 'http://unitsofmeasure.org',
                'unit': 'min',
                'value': 24,
                'comparator': '<'
            }
        )

        session.execute("""
            CREATE TABLE test_age (
                id INTEGER, age fhir_age);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()

        assert 'The age units must be defined in' in str(excinfo.value)

    def test_post_data_with_null_duration_field(
            self, session, TestAgeModel):
        post = TestAgeModel(
            id=1,
            age={}
        )

        session.execute("""
            CREATE TABLE test_age (
                id INTEGER, age fhir_age);""")

        session.add(post)
        register_composites(session.connection())
        session.commit()
        get = session.query(TestAgeModel).first()
        assert get.id == 1
        assert get.age.code is None
