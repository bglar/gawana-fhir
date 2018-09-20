import pytest
from sqlalchemy.exc import StatementError
from sqlalchemy import Column
from fhir_server.elements import primitives


class TestIdField(object):
    def test_valid_id(self):
        result = primitives.IdField().process_bind_param(
            'aa3-g26-k2l-nm3', 'postgres')
        assert result == 'aa3-g26-k2l-nm3'

    def test_empty_string_id(self):
        with pytest.raises(ValueError) as excinfo:
            primitives.IdField().process_bind_param('', 'postgres')

        assert 'Id must have at least 1 character' in str(
            excinfo.value)

    def test_id_more_than_64_chars(self):
        data = 'abc12-efg34-yhu78' * 6
        with pytest.raises(ValueError) as excinfo:
            primitives.IdField().process_bind_param(data, 'postgres')

        assert 'Id field cannot be more than 64 characters' in str(
            excinfo.value)

    def test_id_invalid_chars(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.IdField().process_bind_param('::~', 'postgres')

        assert 'Id: ::~ is not a valid id' in str(
            excinfo.value)

    def test_id_accepts_none_values(self):
        result = primitives.IdField().process_bind_param(None, 'postgres')
        assert result is None

    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = 'circle_test'
            id = Column(primitives.IdField, primary_key=True)
            int_field = Column(primitives.IntegerField)

        session.execute("""
            CREATE TABLE circle_test (
                id TEXT, int_field boolean);""")

        return TestDataTypesModel

    def test_IdField_value_invalid(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=":::",
            int_field=1
        )

        with pytest.raises(StatementError) as excinfo:
            session.add(post_data)
            session.commit()

        assert 'Id: ::: is not a valid id' in str(excinfo.value)
