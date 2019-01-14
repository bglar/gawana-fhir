import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.ratio import RatioField, Ratio as RatioDef


class TestRatio(object):
    @pytest.fixture
    def TestRatioModel(self, Base):
        class TestRatioModel(Base):
            __tablename__ = "test_ratio"
            id = Column(primitives.IntegerField, primary_key=True)
            ratio = Column(RatioField())

        return TestRatioModel

    def test_post_data(self, session, TestRatioModel):
        post = TestRatioModel(
            id=1,
            ratio={
                "denominator": {
                    "code": "code",
                    "system": "system",
                    "unit": "kg",
                    "value": 2.400023,
                    "comparator": "<",
                },
                "numerator": {
                    "code": "code",
                    "system": "system",
                    "unit": "kg",
                    "value": 0.400023,
                    "comparator": ">",
                },
            },
        )

        session.execute(
            """
            CREATE TABLE test_ratio (
                id INTEGER, ratio fhir_ratio);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestRatioModel).first()
        assert get.id == 1
        assert get.ratio.numerator.comparator == ">"

    def test_post_data_with_null_ratio_field(self, session, TestRatioModel):
        post = TestRatioModel(id=1, ratio={})

        session.execute(
            """
            CREATE TABLE test_ratio (
                id INTEGER, ratio fhir_ratio);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestRatioModel).first()
        assert get.id == 1
        assert get.ratio.denominator is None

    @pytest.fixture
    def ProfiledRatio(self):
        class Ratio(RatioDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality["mini"] = 1

                return fields

        return Ratio()()

    @pytest.fixture
    def TestProfiledRatio(self, Base):
        class TestProfiledRatio(Base):
            __tablename__ = "test_ratio"
            id = Column(primitives.IntegerField, primary_key=True)
            ratio = Column(self.ProfiledRatio())

        return TestProfiledRatio

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledRatio()
        denominator = [field for field in fields.columns if field.name == "denominator"]
        numerator = [field for field in fields.columns if field.name == "numerator"]

        assert not denominator[0].nullable
        assert not numerator[0].nullable

    def test_post_data_fields_present(self, session, TestProfiledRatio):
        post = TestProfiledRatio(
            id=1,
            ratio={
                "denominator": {
                    "code": "code",
                    "system": "system",
                    "unit": "kg",
                    "value": 2.400023,
                    "comparator": "<",
                },
                "numerator": {
                    "code": "code",
                    "system": "system",
                    "unit": "kg",
                    "value": 0.400023,
                    "comparator": ">",
                },
            },
        )

        session.execute(
            """
            CREATE TABLE test_ratio (
                id INTEGER, ratio fhir_ratio);"""
        )

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledRatio).first()
        assert get.id == 1
        assert get.ratio.denominator.code == "code"

    def test_fail_to_post_data_missing_fields(self, session, TestProfiledRatio):
        post = TestProfiledRatio(id=1, ratio={})

        session.execute(
            """
            CREATE TABLE test_ratio (
                id INTEGER, ratio fhir_ratio);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ("Field denominator in column fhir_ratio not " "nullable") in str(
            excinfo.value
        )
        assert ("Field numerator in column fhir_ratio not " "nullable") in str(
            excinfo.value
        )
