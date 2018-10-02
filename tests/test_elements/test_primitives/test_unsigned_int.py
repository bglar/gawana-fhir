import uuid
import pytest

from sqlalchemy.exc import StatementError
from sqlalchemy import Column
from fhir_server.elements import primitives


class TestUnsignedIntField(object):
    def test_positive_num(self):
        result = primitives.UnsignedIntField().process_bind_param(
            10, 'postgres')
        assert result == 10

    def test_negative_num(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.UnsignedIntField().process_bind_param(-10, 'postgres')

        assert 'Value -10 must be an int greater than or equal 0' in str(
            excinfo.value)

    def test_zero_is_acceptable(self):
        result = primitives.UnsignedIntField().process_bind_param(0, 'postgres')
        assert result == 0

    def test_none_values(self):
        result = primitives.UnsignedIntField().process_bind_param(
            None, 'postgres')
        assert result is None

    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = 'circle_test'
            id = Column(primitives.IdField, primary_key=True)
            uns_int_field = Column(primitives.UnsignedIntField)

        session.execute("""
            CREATE TABLE circle_test (
                id TEXT, uns_int_field INTEGER);""")

        return TestDataTypesModel

    def test_value_less_than_0(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            uns_int_field=-10
        )

        with pytest.raises(StatementError) as excinfo:
            session.add(post_data)
            session.commit()

        assert 'Value -10 must be an int greater than or equal 0' in str(
            excinfo.value)
