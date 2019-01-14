import uuid
import os
import pytest

from sqlalchemy import Column
from fhir_server.elements import primitives


class TestURIField(object):
    def test_URI_get_col_spec(self):
        result = primitives.URIField().get_col_spec()
        assert result == "URI"

    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = "circle_test"
            id = Column(primitives.IdField, primary_key=True)
            uri_field = Column(primitives.URIField)

        session.execute(
            """
            CREATE TABLE circle_test (
                id TEXT, uri_field uri);"""
        )

        return TestDataTypesModel

    def test_uri_conversion(self, session, TestDataTypesModel):
        id = str(uuid.uuid4())
        post_data = TestDataTypesModel(id=id, uri_field="http://ggaga.daga.com")

        session.add(post_data)
        session.commit()

        get_data = session.query(TestDataTypesModel).first()
        assert get_data.uri_field == "http://ggaga.daga.com"

        result = session.execute(
            """SELECT uri_scheme(circle_test.uri_field)
            FROM circle_test"""
        ).fetchall()
        assert result[0] == ("http",)
