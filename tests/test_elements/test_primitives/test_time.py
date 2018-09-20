import uuid
from datetime import datetime
import pytest

from sqlalchemy.exc import StatementError
from sqlalchemy import Column
from fhir_server.elements import primitives


class TestTimeField(object):
    def test_zero_fill_seconds(self):
        result = primitives.TimeField().process_bind_param('11:22', 'postgres')
        assert result == '11:22:00'

    def test_2400_hrs(self):
        with pytest.raises(ValueError) as excinfo:
            primitives.TimeField().process_bind_param('24:00', 'postgres')

        assert 'Time field expects valid str or time' in str(excinfo.value)

    def test_numeric_values_not_allowed(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.TimeField().process_bind_param(1, 'postgres')

        assert 'The Time 1 is invalid' in str(excinfo.value)

    def test_time_with_timezone(self):
        with pytest.raises(ValueError) as excinfo:
            primitives.TimeField().process_bind_param(
                '22:00:00+00:00', 'postgres')

        assert 'Time field expects valid str or time' in str(excinfo.value)

    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = 'circle_test'
            id = Column(primitives.IdField, primary_key=True)
            time_field = Column(primitives.TimeField)

        session.execute("""
            CREATE TABLE circle_test (
                id TEXT, time_field time);""")

        return TestDataTypesModel

    def test_TimeField_with_date(self, session, TestDataTypesModel):
        now = datetime.now()
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            time_field=str(now.date())
        )

        with pytest.raises(StatementError) as excinfo:
            session.add(post_data)
            session.commit()

        assert ('Time field expects str or time object but %s was given' %
                type(str(now.date()) in str(excinfo.value)))

    def test_time_accept_none_values(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            time_field=None
        )

        session.add(post_data)
        session.commit()

        result = session.query(TestDataTypesModel).first()
        assert result.time_field is None

    def test_time_accept_time_object(self, session, TestDataTypesModel):
        now = datetime.now()
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            time_field=now.time()
        )

        session.add(post_data)
        session.commit()

        result = session.query(TestDataTypesModel).first()
        assert str(result.time_field) == now.time().strftime("%H:%M:%S")
