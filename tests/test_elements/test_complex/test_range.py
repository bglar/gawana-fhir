import pytest

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.range import RangeField, Range as RangeDef


class TestRange(object):
    @pytest.fixture
    def TestRangeModel(self, Base):
        class TestRangeModel(Base):
            __tablename__ = "test_range"
            id = Column(primitives.IntegerField, primary_key=True)
            range = Column(RangeField())

        return TestRangeModel

    def test_post_data(self, session, TestRangeModel):
        post = TestRangeModel(
            id=1,
            range={
                "high": {
                    "code": "code",
                    "system": "system",
                    "unit": "kg",
                    "value": 2.400023,
                },
                "low": {
                    "code": "code",
                    "system": "system",
                    "unit": "kg",
                    "value": 0.400023,
                },
            },
        )

        session.execute(
            """
            CREATE TABLE test_range (
                id INTEGER, range fhir_range);"""
        )
        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestRangeModel).first()
        assert get.id == 1
        assert get.range.high.unit == "kg"

    def test_post_fails_if_high_less_than_low(self, session, TestRangeModel):
        post = TestRangeModel(
            id=1,
            range={
                "high": {
                    "code": "code",
                    "system": "system",
                    "unit": "kg",
                    "value": 2.400023,
                },
                "low": {
                    "code": "code",
                    "system": "system",
                    "unit": "kg",
                    "value": 10.400023,
                },
            },
        )

        session.execute(
            """
            CREATE TABLE test_range (
                id INTEGER, range fhir_range);"""
        )
        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ("low_val cannot be > than high_val") in str(excinfo.value)

    def test_post_fails_if_high_and_low_units_dont_match(self, session, TestRangeModel):
        post = TestRangeModel(
            id=1,
            range={
                "high": {
                    "code": "code",
                    "system": "system",
                    "unit": "kg",
                    "value": 2.400023,
                },
                "low": {
                    "code": "code",
                    "system": "system",
                    "unit": "g",
                    "value": 0.400023,
                },
            },
        )

        session.execute(
            """
            CREATE TABLE test_range (
                id INTEGER, range fhir_range);"""
        )
        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ("units for low and high should match") in str(excinfo.value)

    def test_post_fails_if_high_and_low_code_dont_match(self, session, TestRangeModel):
        post = TestRangeModel(
            id=1,
            range={
                "high": {
                    "code": "code",
                    "system": "system",
                    "unit": "kg",
                    "value": 2.400023,
                },
                "low": {
                    "code": "codeyapili",
                    "system": "system",
                    "unit": "kg",
                    "value": 0.400023,
                },
            },
        )

        session.execute(
            """
            CREATE TABLE test_range (
                id INTEGER, range fhir_range);"""
        )
        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ("codes for low and high should match") in str(excinfo.value)

    def test_post_fails_if_high_and_low_system_dont_match(
        self, session, TestRangeModel
    ):
        post = TestRangeModel(
            id=1,
            range={
                "high": {
                    "code": "code",
                    "system": "system",
                    "unit": "kg",
                    "value": 2.400023,
                },
                "low": {
                    "code": "code",
                    "system": "system2",
                    "unit": "kg",
                    "value": 0.400023,
                },
            },
        )

        session.execute(
            """
            CREATE TABLE test_range (
                id INTEGER, range fhir_range);"""
        )
        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ("systems for low and high should match") in str(excinfo.value)

    def test_post_data_with_null_range_field(self, session, TestRangeModel):
        post = TestRangeModel(id=1, range={})

        session.execute(
            """
            CREATE TABLE test_range (
                id INTEGER, range fhir_range);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestRangeModel).first()
        assert get.id == 1
        assert get.range.high is None

    @pytest.fixture
    def ProfiledRange(self):
        class Range(RangeDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality["mini"] = 1

                return fields

        return Range()()

    @pytest.fixture
    def TestProfiledRange(self, Base):
        class TestProfiledRange(Base):
            __tablename__ = "test_range"
            id = Column(primitives.IntegerField, primary_key=True)
            range = Column(self.ProfiledRange())

        return TestProfiledRange

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledRange()
        high = [field for field in fields.columns if field.name == "high"]
        low = [field for field in fields.columns if field.name == "low"]

        assert not high[0].nullable
        assert not low[0].nullable

    def test_post_data_fields_present(self, session, TestProfiledRange):
        post = TestProfiledRange(
            id=1,
            range={
                "high": {
                    "code": "code",
                    "system": "system",
                    "unit": "kg",
                    "value": 2.400023,
                },
                "low": {
                    "code": "code",
                    "system": "system",
                    "unit": "kg",
                    "value": 0.400023,
                },
            },
        )

        session.execute(
            """
            CREATE TABLE test_range (
                id INTEGER, range fhir_range);"""
        )

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledRange).first()
        assert get.id == 1
        assert get.range.high.code == "code"

    def test_fail_to_post_data_missing_fields(self, session, TestProfiledRange):
        post = TestProfiledRange(id=1, range={})

        session.execute(
            """
            CREATE TABLE test_range (
                id INTEGER, range fhir_range);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ("Field high in column fhir_range not " "nullable") in str(excinfo.value)
        assert ("Field low in column fhir_range not " "nullable") in str(excinfo.value)
