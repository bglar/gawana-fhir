from decimal import Decimal
import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.count import (
    Count as CountDef, CountField)


class TestCount(object):

    @pytest.fixture
    def TestCountModel(self, Base):
        class TestCountModel(Base):
            __tablename__ = 'test_count'
            id = Column(primitives.IntegerField, primary_key=True)
            count = Column(CountField())
        return TestCountModel

    def test_post_data(self, session, TestCountModel):
        post = TestCountModel(
            id=1,
            count={
                'code': 'code',
                'system': 'system',
                'value': 2.400023,
                'comparator': '<'
            }
        )

        session.execute("""
            CREATE TABLE test_count (
                id INTEGER, count fhir_count);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestCountModel).first()
        assert get.id == 1
        assert get.count.value == Decimal('2.400023')

    def test_post_data_with_null_count_field(
            self, session, TestCountModel):
        post = TestCountModel(
            id=1,
            count={}
        )

        session.execute("""
            CREATE TABLE test_count (
                id INTEGER, count fhir_count);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestCountModel).first()
        assert get.id == 1
        assert get.count.code is None
