import uuid
import pytest
import pytz
from pytz.exceptions import AmbiguousTimeError
from datetime import datetime

from sqlalchemy.exc import StatementError
from sqlalchemy import Column
from fhir_server.elements import primitives


class TestDateTimeField(object):
    def test_only_year(self):
        result = primitives.DateTimeField().process_bind_param(
            '2011', 'postgres')
        assert result == '2011'

    def test_only_month_and_year(self):
        result = primitives.DateTimeField().process_bind_param(
            '2011-05', 'postgres')
        assert result == '2011-05'

    def test_only_day_month_and_year(self):
        result = primitives.DateTimeField().process_bind_param(
            '2011-05-24', 'postgres')
        assert result == '2011-05-24'

    def test_time_to_seconds_no_timezone(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.DateTimeField().process_bind_param(
                '2011-05-24T22:00:02', 'postgres')

        assert 'The DateTime 2011-05-24T22:00:02 is invalid' in str(
            excinfo.value)

    def test_time_no_seconds(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.DateTimeField().process_bind_param(
                '2011-05-24T22:00', 'postgres')

        assert 'The DateTime 2011-05-24T22:00 is invalid' in str(
            excinfo.value)

    def test_not_allow_2400_hrs(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.DateTimeField().process_bind_param(
                '2011-05-24T24:00:00', 'postgres')

        assert 'The DateTime 2011-05-24T24:00:00 is invalid' in str(
            excinfo.value)

    def test_time_with_timezone(self):
        result = primitives.DateTimeField().process_bind_param(
            '2011-05-24T22:00:00+03:14', 'postgres')
        assert result == '2011-05-24T22:00:00+03:14'

    def test_code_accept_none_values(self):
        result = primitives.DateTimeField().process_bind_param(None, 'postgres')
        assert result is None

    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = 'circle_test'
            id = Column(primitives.IdField, primary_key=True)
            date_time_field = Column(primitives.DateTimeField)

        session.execute("""
            CREATE TABLE circle_test (
                id TEXT, date_time_field timestamp with time zone);""")

        return TestDataTypesModel

    def test_invalid_time_is_rejected(self, session, TestDataTypesModel):
        siku_mbaya = "2002-10-27T01:30:00"
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            date_time_field=siku_mbaya
        )

        with pytest.raises(StatementError) as excinfo:
            session.add(post_data)
            session.commit()

        assert (
            'The DateTime %s is invalid' % siku_mbaya) in str(excinfo.value)

    def test_DateTimeField_no_timezone(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            date_time_field="Sema"
        )

        with pytest.raises(StatementError) as excinfo:
            session.add(post_data)
            session.commit()

        assert 'The DateTime Sema is invalid' in str(excinfo.value)

    def test_seconds_prefilled(self, session, TestDataTypesModel):
        id = str(uuid.uuid4())
        post_data = TestDataTypesModel(
            id=id,
            date_time_field="2011-05-24T22:25+03:00"
        )
        session.add(post_data)
        session.commit()

        get_data = session.query(TestDataTypesModel).first()
        assert get_data.date_time_field == post_data.date_time_field

    def test_validate_local_times_with_int(self):
        result = primitives.validate_local_times(1)
        assert result is None

    def test_invalid_local_times_with_date_obj(self):
        now = datetime(2002, 10, 27, 1, 30, 00, 34525, tzinfo=pytz.UTC)

        with pytest.raises(AmbiguousTimeError) as excinfo:
            primitives.validate_local_times(now)
        assert 'Ambiguous Time Error' in str(excinfo.value)

    def test_valid_local_times_with_date_obj(self):
        now = datetime(2002, 9, 27, 1, 30, 00, 34525)
        result = primitives.validate_local_times(now)
        assert result is None
