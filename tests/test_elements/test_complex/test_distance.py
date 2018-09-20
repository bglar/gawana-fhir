from decimal import Decimal
import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.distance import (
    Distance as DistanceDef, DistanceField)


class TestDistance(object):

    @pytest.fixture
    def TestDistanceModel(self, Base):
        class TestDistanceModel(Base):
            __tablename__ = 'test_distance'
            id = Column(primitives.IntegerField, primary_key=True)
            distance = Column(DistanceField())
        return TestDistanceModel

    def test_post_data(self, session, TestDistanceModel):
        post = TestDistanceModel(
            id=1,
            distance={
                'code': 'code',
                'system': 'system',
                'unit': 'kg',
                'value': 2.400023,
                'comparator': '<'
            }
        )

        session.execute("""
            CREATE TABLE test_distance (
                id INTEGER, distance fhir_distance);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestDistanceModel).first()
        assert get.id == 1
        assert get.distance.value == Decimal('2.400023')

    def test_post_data_with_null_distance_field(
            self, session, TestDistanceModel):
        post = TestDistanceModel(
            id=1,
            distance={}
        )

        session.execute("""
            CREATE TABLE test_distance (
                id INTEGER, distance fhir_distance);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestDistanceModel).first()
        assert get.id == 1
        assert get.distance.code is None
