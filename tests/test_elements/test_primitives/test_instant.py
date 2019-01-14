import uuid
import pytest
from datetime import datetime
import pytz

from sqlalchemy.exc import StatementError
from sqlalchemy import Column
from fhir_server.elements import primitives


class TestInstantField(object):
    def test_time_no_timezone(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.InstantField().process_bind_param(
                "2011-05-24T22:00:02", "postgres"
            )

        assert ("The Instant 2011-05-24T22:00:02 is invalid") in str(excinfo.value)

    def test_time_no_seconds(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.InstantField().process_bind_param("2011-05-24T22:00", "postgres")

        assert ("The Instant 2011-05-24T22:00 is invalid") in str(excinfo.value)

    def test_2400_hrs(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.InstantField().process_bind_param(
                "2011-05-24T24:00:00", "postgres"
            )

        assert ("The Instant 2011-05-24T24:00:00 is invalid") in str(excinfo.value)

    def test_time_with_timezone(self):
        result = primitives.InstantField().process_bind_param(
            "2011-05-24T22:00:00+0314", "postgres"
        )
        assert result == "2011-05-24T22:00:00+0314"

    def test_datetime_value_is_converted_to_date_string(self):
        now = pytz.utc.localize(datetime.utcnow())
        result = primitives.InstantField().process_bind_param(now, "postgres")
        assert result == datetime.strftime(now, "%Y-%m-%dT%H:%M:%S%z")

    def test_instant_accept_none_values(self):
        result = primitives.InstantField().process_bind_param(None, "postgres")
        assert result is None

    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = "circle_test"
            id = Column(primitives.IdField, primary_key=True)
            instant_field = Column(primitives.InstantField)

        session.execute(
            """
            CREATE TABLE circle_test (
                id TEXT, instant_field timestamp with time zone);"""
        )

        return TestDataTypesModel

    def test_Instant_invalid(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(id=str(uuid.uuid4()), instant_field="Sema")

        with pytest.raises(StatementError) as excinfo:
            session.add(post_data)
            session.commit()
        assert ("The Instant Sema is invalid") in str(excinfo.value)

    def test_seconds_prefilled(self, session, TestDataTypesModel):
        id = str(uuid.uuid4())
        post_data = TestDataTypesModel(id=id, instant_field="2011-05-24T22:25+0300")
        session.add(post_data)
        session.commit()

        get_data = session.query(TestDataTypesModel).first()
        assert get_data.instant_field == post_data.instant_field
