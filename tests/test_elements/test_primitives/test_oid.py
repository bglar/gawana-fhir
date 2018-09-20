import uuid
import pytest

from sqlalchemy.exc import StatementError
from sqlalchemy import Column
from fhir_server.elements import primitives


class TestOIDField(object):
    def test_valid_oid(self):
        process_func = primitives.OIDField().bind_processor('postgres')
        result = process_func('urn:oid:1.2.3.4.5')
        assert result == 'urn:oid:1.2.3.4.5'

    def test_oid_accept_none_values(self):
        process_func = primitives.OIDField().bind_processor('postgres')
        result = process_func(None)
        assert result is None

    def test_oid_missing_urn(self):
        process_func = primitives.OIDField().bind_processor('postgres')
        with pytest.raises(TypeError) as excinfo:
            process_func('oid:1.2.3.4.5')

        assert ('This OID is invalid') in str(excinfo.value)

    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = 'circle_test'
            id = Column(primitives.IdField, primary_key=True)
            oid_field = Column(primitives.OIDField)

        session.execute("""
            CREATE TABLE circle_test (
                id TEXT, oid_field URI);""")

        return TestDataTypesModel

    def test_invalid_oid(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            oid_field='1.2.3.4.5'
        )

        with pytest.raises(StatementError) as excinfo:
            session.add(post_data)
            session.commit()

        assert ('This OID is invalid') in str(
            excinfo.value)
