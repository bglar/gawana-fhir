import uuid
import pytest

from sqlalchemy.exc import StatementError
from sqlalchemy import Column
from fhir_server.elements import primitives


class TestDateField(object):
    def test_only_year(self):
        result = primitives.DateField().process_bind_param("2011", "postgres")
        assert result == "2011"

    def test_only_month_and_year(self):
        result = primitives.DateField().process_bind_param("2011-05", "postgres")
        assert result == "2011-05"

    def test_only_day_month_and_year(self):
        result = primitives.DateField().process_bind_param("2011-05-24", "postgres")
        assert result == "2011-05-24"

    def test_time(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.DateField().process_bind_param("2011-05-24T23:00:00", "postgres")

        assert ("The Date 2011-05-24T23:00:00 is invalid") in str(excinfo.value)

    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = "circle_test"
            id = Column(primitives.IdField, primary_key=True)
            date_field = Column(primitives.DateField)

        session.execute(
            """
            CREATE TABLE circle_test (
                id TEXT, date_field date);"""
        )

        return TestDataTypesModel

    def test_DateField_invalid(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(id=str(uuid.uuid4()), date_field="2011-05-33")

        session.add(post_data)
        with pytest.raises(StatementError) as excinfo:
            session.commit()

        assert ("The Date %s is invalid" % post_data.date_field) in str(excinfo.value)

    def test_date_accepts_none_values(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(id=str(uuid.uuid4()), date_field=None)

        session.add(post_data)
        session.commit()

        result = session.query(TestDataTypesModel).first()
        assert result.date_field is None
