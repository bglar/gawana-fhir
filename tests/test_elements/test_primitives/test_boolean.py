import uuid
import pytest

from sqlalchemy.exc import ProgrammingError
from sqlalchemy import Column
from fhir_server.elements import primitives


class TestBooleanField(object):
    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = 'circle_test'
            id = Column(primitives.IdField, primary_key=True)
            bool_field = Column(primitives.BooleanField)

        session.execute("""
            CREATE TABLE circle_test (
                id TEXT, bool_field boolean);""")

        return TestDataTypesModel

    def test_true_value(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            bool_field=True
        )
        session.add(post_data)
        session.commit()

        get_data = session.query(TestDataTypesModel).all()
        assert post_data in get_data

    def test_accept_Y_value(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            bool_field='Y'
        )
        session.add(post_data)
        session.commit()

        get_data = session.query(TestDataTypesModel).all()
        assert post_data in get_data

    def test_accept_N_value(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            bool_field='N'
        )
        session.add(post_data)
        session.commit()

        get_data = session.query(TestDataTypesModel).all()
        assert post_data in get_data

    def test_false_value(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            bool_field=False
        )
        session.add(post_data)
        session.commit()

        get_data = session.query(TestDataTypesModel).all()
        assert post_data in get_data

    def test_must_not_accept_1(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            bool_field=1
        )
        session.add(post_data)
        with pytest.raises(ProgrammingError) as excinfo:
            session.commit()

        assert ('column "bool_field" is of type boolean but expression is '
                'of type integer') in str(excinfo.value)
        session.close()

    def test_must_not_accept_0(self, session, TestDataTypesModel):
        post_data = TestDataTypesModel(
            id=str(uuid.uuid4()),
            bool_field=0
        )
        session.add(post_data)
        with pytest.raises(ProgrammingError) as excinfo:
            session.commit()

        assert ('column "bool_field" is of type boolean but expression is '
                'of type integer') in str(excinfo.value)
