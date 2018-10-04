import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.period import (
    PeriodField, Period as PeriodDef)


class TestPeriod(object):

    @pytest.fixture
    def TestPeriodModel(self, Base):
        class TestPeriodModel(Base):
            __tablename__ = 'test_period'
            id = Column(primitives.IntegerField, primary_key=True)
            period = Column(PeriodField(), nullable=False)
        return TestPeriodModel

    def test_post_data(self, session, TestPeriodModel):
        post = TestPeriodModel(
            id=1,
            period={
                'start': '2011-05-24',
                'end': '2011-06-24'
            }
        )

        post2 = TestPeriodModel(
            id=2,
            period=None
        )

        session.execute("""
            CREATE TABLE test_period (
                id INTEGER, period fhir_period);""")

        register_composites(session.connection())
        session.add(post)
        session.add(post2)
        session.commit()
        get = session.query(TestPeriodModel).first()
        assert get.id == 1
        assert str(get.period.start) == '2011-05-24 00:00:00+03:00'

    def test_posting_str_data_on_composite_fields(
            self, session, TestPeriodModel):
        post = TestPeriodModel(
            id=1,
            period="test"
        )

        post2 = TestPeriodModel(
            id=2
        )

        session.execute("""
            CREATE TABLE test_period (
                id INTEGER, period fhir_period);""")

        register_composites(session.connection())
        session.add(post)
        session.add(post2)
        session.commit()
        get = session.query(TestPeriodModel).first()
        assert get.id == 1
        assert get.period.start is None

    def test_post_data_with_null_period_field(
            self, session, TestPeriodModel):
        post = TestPeriodModel(
            id=1,
            period={}
        )

        session.execute("""
            CREATE TABLE test_period (
                id INTEGER, period fhir_period);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestPeriodModel).first()
        assert get.id == 1
        assert get.period.end is None

    @pytest.fixture
    def ProfiledPeriod(self):
        class Period(PeriodDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality['mini'] = 1

                return fields

        return Period()()

    @pytest.fixture
    def TestProfiledPeriod(self, Base):
        class TestProfiledPeriod(Base):
            __tablename__ = 'test_period'
            id = Column(primitives.IntegerField, primary_key=True)
            period = Column(self.ProfiledPeriod())
        return TestProfiledPeriod

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledPeriod()
        end = [field for field in fields.columns if field.name == 'end']
        start = [
            field for field in fields.columns if field.name == 'start']

        assert not start[0].nullable
        assert not end[0].nullable

    def test_post_data_fields_present(
            self, session, TestProfiledPeriod):
        post = TestProfiledPeriod(
            id=1,
            period={
                'start': '2011-05-24',
                'end': '2011-06-24'
            }
        )

        session.execute("""
            CREATE TABLE test_period (
                id INTEGER, period fhir_period);""")

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledPeriod).first()
        assert get.id == 1
        assert str(get.period.start) == '2011-05-24 00:00:00+03:00'

    def test_fail_to_post_data_missing_fields(
            self, session, TestProfiledPeriod):
        post = TestProfiledPeriod(
            id=1,
            period={}
        )

        session.execute("""
            CREATE TABLE test_period (
                id INTEGER, period fhir_period);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('Field start in column fhir_period not '
                'nullable') in str(excinfo.value)
        assert ('Field end in column fhir_period not '
                'nullable') in str(excinfo.value)
