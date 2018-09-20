from decimal import Decimal
import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.duration import (
    Duration as DurationDef, DurationField)


class TestDuration(object):

    @pytest.fixture
    def TestDurationModel(self, Base):
        class TestDurationModel(Base):
            __tablename__ = 'test_duration'
            id = Column(primitives.IntegerField, primary_key=True)
            duration = Column(DurationField())
        return TestDurationModel

    def test_post_data(self, session, TestDurationModel):
        post = TestDurationModel(
            id=1,
            duration={
                'code': 'min',
                'system': 'system',
                'unit': 'kg',
                'value': 2.400023,
                'comparator': '<'
            }
        )

        session.execute("""
            CREATE TABLE test_duration (
                id INTEGER, duration fhir_duration);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestDurationModel).first()
        assert get.id == 1
        assert get.duration.value == Decimal('2.400023')

    def test_reject_data_with_code_not_in_valuesets(
            self, session, TestDurationModel):
        post = TestDurationModel(
            id=1,
            duration={
                'code': 'notinvalueset',
                'system': 'system',
                'unit': 'kg',
                'value': 2.400023,
                'comparator': '<'
            }
        )

        session.execute("""
            CREATE TABLE test_duration (
                id INTEGER, duration fhir_duration);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()

        assert 'The duration units must be defined in' in str(excinfo.value)

    def test_post_data_with_null_duration_field(
            self, session, TestDurationModel):
        post = TestDurationModel(
            id=1,
            duration={}
        )

        session.execute("""
            CREATE TABLE test_duration (
                id INTEGER, duration fhir_duration);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestDurationModel).first()
        assert get.id == 1
        assert get.duration.code is None
