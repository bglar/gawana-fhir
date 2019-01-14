import uuid
import pytest

from sqlalchemy.exc import DataError
from sqlalchemy import Column
from fhir_server.elements import primitives


class TestIntegerField(object):
    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = "circle_test"
            id = Column(primitives.IdField, primary_key=True)
            int_field = Column(primitives.IntegerField)

        session.execute(
            """
            CREATE TABLE circle_test (
                id TEXT, int_field INTEGER);"""
        )

        return TestDataTypesModel

    def test_min_value(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(id=str(uuid.uuid4()), int_field=-2147483648)
        session.add(post_data)
        session.commit()

        get_data = session.query(TestDataTypesModel).all()
        assert post_data in get_data

    def test_max_value(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(id=str(uuid.uuid4()), int_field=2147483647)
        session.add(post_data)
        session.commit()

        get_data = session.query(TestDataTypesModel).all()
        assert post_data in get_data

    def test_not_more_than_max_value(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(id=str(uuid.uuid4()), int_field=21474836478)
        with pytest.raises(DataError) as excinfo:
            session.add(post_data)
            session.commit()

        assert ("(psycopg2.DataError) integer out of range") in str(excinfo.value)

    def test__not_less_than_min_value(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(id=str(uuid.uuid4()), int_field=-21474836478)
        with pytest.raises(DataError) as excinfo:
            session.add(post_data)
            session.commit()

        assert ("(psycopg2.DataError) integer out of range") in str(excinfo.value)

    def test_string_int_value(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(id=str(uuid.uuid4()), int_field="214748")
        session.add(post_data)
        session.commit()

        get_data = session.query(TestDataTypesModel).all()
        assert post_data in get_data
