import uuid
import pytest

from sqlalchemy.exc import StatementError
from sqlalchemy import Column
from fhir_server.elements import primitives


class TestPositiveIntField(object):
    def test_positive_num(self):
        result = primitives.PositiveIntField().process_bind_param(
            10, 'postgres')
        assert result == 10

    def test_negative_num(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.PositiveIntField().process_bind_param(-10, 'postgres')

        assert 'Value -10 must be a positive integer greater than 0' in str(
            excinfo.value)

    def test_zero(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.PositiveIntField().process_bind_param(0, 'postgres')

        assert 'Value 0 must be a positive integer greater than 0' in str(
            excinfo.value)

    def test_none(self):
        result = primitives.PositiveIntField().process_bind_param(
            None, 'postgres')

        assert result is None

    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = 'circle_test'
            id = Column(primitives.IdField, primary_key=True)
            pos_int_field = Column(primitives.PositiveIntField)

        session.execute("""
            CREATE TABLE circle_test (
                id TEXT, pos_int_field INTEGER);""")

        return TestDataTypesModel

    def test_correct_data(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            pos_int_field=12
        )
        session.add(post_data)
        session.commit()

        get_data = session.query(TestDataTypesModel).all()
        assert post_data in get_data

    def test_value_less_than_0(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            pos_int_field=-10
        )

        with pytest.raises(StatementError) as excinfo:
            session.add(post_data)
            session.commit()

        assert 'Value -10 must be a positive integer greater than 0' in str(
            excinfo.value)

    def test_value_equal_0(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            pos_int_field=0
        )

        with pytest.raises(StatementError) as excinfo:
            session.add(post_data)
            session.commit()

        assert 'Value 0 must be a positive integer greater than 0' in str(
            excinfo.value)
