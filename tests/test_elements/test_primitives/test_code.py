import uuid
import sys

from sqlalchemy.exc import StatementError
from sqlalchemy import Column
import pytest
from fhir_server.elements import primitives


class TestCodeField(object):
    def test_valid_code(self):
        result = primitives.CodeField().process_bind_param('10', 'postgres')
        assert result == '10'

    def test_accept_none_as_value(self):
        result = primitives.CodeField().process_bind_param(None, 'postgres')
        assert result is None

    def test_code_less_than_1char(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.CodeField().process_bind_param('', 'postgres')

        assert 'This Code:  is invalid' in str(excinfo.value)

    def test_code_no_leading_whitespaces(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.CodeField().process_bind_param(' 2561-1hbw', 'postgres')

        assert 'This Code:  2561-1hbw' in str(excinfo.value)

    def test_code_no_trailing_whitespaces(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.CodeField().process_bind_param('2561-1hbw  ', 'postgres')

        assert 'This Code: 2561-1hbw' in str(excinfo.value)

    def test_code_no_internal_whitespaces(self):
        with pytest.raises(TypeError) as err:
            primitives.CodeField().process_bind_param(
                'my new     text', 'postgres')
        assert ('Code must not have a whitespace more than a single'
                ' character') in str(err.value)

    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = 'circle_test'
            id = Column(primitives.IdField, primary_key=True)
            code_field = Column(primitives.CodeField)

        session.execute("""
            CREATE TABLE circle_test (
                id TEXT, code_field TEXT);""")

        return TestDataTypesModel

    def test_empty_string_invalid(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            code_field='',
        )

        session.add(post_data)
        with pytest.raises(StatementError) as excinfo:
            session.commit()

        assert 'This Code:  is invalid' in str(excinfo.value)

    def test_code_not_larger_than_1MB(self, session, TestDataTypesModel):
        large_str = 'abcde' * 1000000
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            code_field=large_str
        )

        assert sys.getsizeof(large_str) > 1048576
        with pytest.raises(StatementError) as excinfo:
            session.add(post_data)
            session.commit()

        assert ('Code value must not exceed 1MB') in str(excinfo.value)
