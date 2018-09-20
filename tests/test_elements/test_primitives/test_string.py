import uuid
import sys
import pytest

from sqlalchemy.exc import StatementError
from sqlalchemy import Column
from fhir_server.elements import primitives


class TestStringField(object):
    def test_valid_string(self):
        result = primitives.StringField().process_bind_param(
            'my test string', 'postgres')
        assert result == 'my test string'

    def test_string_must_be_unicode(self):
        byte_str = 'some test string'.encode('utf-8')
        with pytest.raises(TypeError) as excinfo:
            primitives.StringField().process_bind_param(byte_str, 'postgres')

        assert ('This field expects unicode string') in str(
            excinfo.value)

    def test_string_must_not_be_bytes(self):
        with pytest.raises(TypeError) as excinfo:
            primitives.StringField().process_bind_param(b'byte_str', 'postgres')

        assert ('This field expects unicode string') in str(
            excinfo.value)

    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = 'circle_test'
            id = Column(primitives.IdField, primary_key=True)
            str_field = Column(primitives.StringField)

        session.execute("""
            CREATE TABLE circle_test (
                id TEXT, bool_field TEXT);""")

        return TestDataTypesModel

    def test_string_not_larger_than_1MB(self, session, TestDataTypesModel):
        large_str = 'abcde' * 1000000
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            str_field=large_str
        )

        assert sys.getsizeof(large_str) > 1048576
        with pytest.raises(StatementError) as excinfo:
            session.add(post_data)
            session.commit()

        assert ('String value must not exceed 1MB') in str(excinfo.value)
