from decimal import Decimal
import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.sampleddata import (
    SampledDataField, SampledData as SampledDataDef)


class TestSampledData(object):

    @pytest.fixture
    def TestSampledDataModel(self, Base):
        class TestSampledDataModel(Base):
            __tablename__ = 'test_sampleddata'
            id = Column(primitives.IntegerField, primary_key=True)
            sampleddata = Column(SampledDataField())
        return TestSampledDataModel

    def test_post_data(self, session, TestSampledDataModel):
        post = TestSampledDataModel(
            id=1,
            sampleddata={
                'data': '2.1E',
                'dimensions': 3,
                'factor': 0.2333,
                'lowerLimit': 1.5,
                'period': 0.1,
                'upperLimit': 7.9,
                'origin': {
                    'code': 'code',
                    'system': 'system',
                    'unit': 'kg',
                    'value': 2.400023
                }
            }
        )

        session.execute("""
            CREATE TABLE test_sampleddata (
                id INTEGER, sampleddata fhir_sampleddata);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestSampledDataModel).first()
        assert get.id == 1
        assert get.sampleddata.upperLimit == Decimal('7.9')

    def test_reject_invalid_data_field(self, session, TestSampledDataModel):
        post = TestSampledDataModel(
            id=1,
            sampleddata={
                'data': '2.1K',
                'dimensions': 3,
                'factor': 0.2333,
                'lowerLimit': 1.5,
                'period': 0.1,
                'upperLimit': 7.9,
                'origin': {
                    'code': 'code',
                    'system': 'system',
                    'unit': 'kg',
                    'value': 2.400023
                }
            }
        )

        session.execute("""
            CREATE TABLE test_sampleddata (
                id INTEGER, sampleddata fhir_sampleddata);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'Data should be composed of decimal values with spaces' in str(
            excinfo.value)

    def test_post_data_with_null_sampleddata_field(
            self, session, TestSampledDataModel):
        post = TestSampledDataModel(
            id=1,
            sampleddata={
                'data': '2.3U',
                'dimensions': 3,
                'period': 0.1,
                'origin': {
                    'code': 'code',
                    'system': 'system',
                    'unit': 'kg',
                    'value': 2.400023
                }
            }
        )

        session.execute("""
            CREATE TABLE test_sampleddata (
                id INTEGER, sampleddata fhir_sampleddata);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestSampledDataModel).first()
        assert get.id == 1
        assert get.sampleddata.factor is None

    def test_fail_to_post_data_if_there_is_more_than_one_whitespace(
            self, session, TestProfiledSampledData):
        post = TestProfiledSampledData(
            id=1,
            sampleddata={
                'data': '2.1   E',
                'dimensions': 3,
                'factor': 0.2333,
                'lowerLimit': 1.5,
                'period': 0.1,
                'upperLimit': 7.9,
                'origin': {
                    'code': 'code',
                    'system': 'system',
                    'unit': 'kg',
                    'value': 2.400023
                }
            }
        )

        session.execute("""
            CREATE TABLE test_sampleddata (
                id INTEGER, sampleddata fhir_sampleddata);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('data in sampleddata must not have more than 1 '
                'whitespace') in str(excinfo.value)

    @pytest.fixture
    def ProfiledSampledData(self):
        class SampledData(SampledDataDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality['mini'] = 1

                return fields

        return SampledData()()

    @pytest.fixture
    def TestProfiledSampledData(self, Base):
        class TestProfiledSampledData(Base):
            __tablename__ = 'test_sampleddata'
            id = Column(primitives.IntegerField, primary_key=True)
            sampleddata = Column(self.ProfiledSampledData())
        return TestProfiledSampledData

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledSampledData()
        factor = [field for field in fields.columns if field.name == 'factor']
        lowerLimit = [
            field for field in fields.columns if field.name == 'lowerLimit']
        upperLimit = [
            field for field in fields.columns if field.name == 'upperLimit']

        assert not factor[0].nullable
        assert not lowerLimit[0].nullable
        assert not upperLimit[0].nullable

    def test_post_data_fields_present(
            self, session, TestProfiledSampledData):
        post = TestProfiledSampledData(
            id=1,
            sampleddata={
                'data': '2.3L',
                'dimensions': 3,
                'factor': 0.2333,
                'lowerLimit': 1.5,
                'period': 0.1,
                'upperLimit': 7.9,
                'origin': {
                    'code': 'code',
                    'system': 'system',
                    'unit': 'kg',
                    'value': 2.400023
                }
            }
        )

        session.execute("""
            CREATE TABLE test_sampleddata (
                id INTEGER, sampleddata fhir_sampleddata);""")

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledSampledData).first()
        assert get.id == 1
        assert get.sampleddata.data == '2.3L'

    def test_fail_to_post_data_missing_fields(
            self, session, TestProfiledSampledData):
        post = TestProfiledSampledData(
            id=1,
            sampleddata={
                'data': '2.5 ',
                'dimensions': 3,
                'period': 0.1,
                'origin': {
                    'code': 'code',
                    'system': 'system',
                    'unit': 'kg',
                    'value': 2.400023
                }
            }
        )

        session.execute("""
            CREATE TABLE test_sampleddata (
                id INTEGER, sampleddata fhir_sampleddata);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('Field factor in column fhir_sampleddata not '
                'nullable') in str(excinfo.value)
        assert ('Field lowerLimit in column fhir_sampleddata not '
                'nullable') in str(excinfo.value)
        assert ('Field upperLimit in column fhir_sampleddata not '
                'nullable') in str(excinfo.value)
