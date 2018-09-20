import pytest

from sqlalchemy import Column
from sqlalchemy_utils import register_composites
from sqlalchemy.exc import StatementError

from fhir_server.elements import primitives
from fhir_server.elements.complex.coding import (
    CodingField, Coding as CodingDef)


class TestCoding(object):

    @pytest.fixture
    def TestCodingModel(self, Base):
        class TestCodingModel(Base):
            __tablename__ = 'test_coding'
            id = Column(primitives.IntegerField, primary_key=True)
            coding = Column(CodingField())
        return TestCodingModel

    def test_post_data(self, session, TestCodingModel):
        post = TestCodingModel(
            id=1,
            coding={
                'code': 'dkls323-3223hj',
                'display': 'display',
                'system': 'http://loinc.org',
                'userSelected': True,
                'version': '2.3'
            }
        )

        session.execute("""
            CREATE TABLE test_coding (
                id INTEGER, coding fhir_coding);""")

        session.add(post)
        register_composites(session.connection())
        session.commit()
        get = session.query(TestCodingModel).first()
        assert get.id == 1
        assert get.coding.display == 'display'

    def test_reject_data_with_system_not_sanctioned_url(
            self, session, TestCodingModel):
        post = TestCodingModel(
            id=1,
            coding={
                'code': 'dkls323-3223hj',
                'display': 'display',
                'system': 'invalid',
                'userSelected': True,
                'version': '2.3'
            }
        )

        session.execute("""
            CREATE TABLE test_coding (
                id INTEGER, coding fhir_coding);""")

        with pytest.raises(StatementError) as excinfo:
            session.add(post)
            session.commit()
        assert ("Use a sanctioned uri from [http://hl7.org/fhir/"
                "terminologies-systems.html]") in str(excinfo.value)

    def test_post_data_with_null_coding_field(
            self, session, TestCodingModel):
        post = TestCodingModel(
            id=1,
            coding={}
        )

        session.execute("""
            CREATE TABLE test_coding (
                id INTEGER, coding fhir_coding);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestCodingModel).first()
        assert get.id == 1
        assert get.coding.code is None

    @pytest.fixture
    def ProfiledCoding(self):
        class Coding(CodingDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality['mini'] = 1

                return fields

        return Coding()()

    @pytest.fixture
    def TestProfiledCoding(self, Base):
        class TestProfiledCoding(Base):
            __tablename__ = 'test_coding'
            id = Column(primitives.IntegerField, primary_key=True)
            coding = Column(self.ProfiledCoding())
        return TestProfiledCoding

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledCoding()
        code = [field for field in fields.columns if field.name == 'code']
        display = [
            field for field in fields.columns if field.name == 'display']
        system = [field for field in fields.columns if field.name == 'system']
        userSelected = [
            field for field in fields.columns if field.name == 'userSelected']
        version = [
            field for field in fields.columns if field.name == 'version']

        assert not code[0].nullable
        assert not display[0].nullable
        assert not system[0].nullable
        assert not userSelected[0].nullable
        assert not version[0].nullable

    def test_post_data_fields_present(
            self, session, TestProfiledCoding):
        post = TestProfiledCoding(
            id=1,
            coding={
                'code': 'dkls323-3223hj',
                'display': 'display',
                'system': 'http://loinc.org',
                'userSelected': True,
                'version': '2.3'
            }
        )

        session.execute("""
            CREATE TABLE test_coding (
                id INTEGER, coding fhir_coding);""")

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledCoding).first()
        assert get.id == 1
        assert get.coding.code == 'dkls323-3223hj'

    def test_fail_to_post_data_missing_fields(
            self, session, TestProfiledCoding):
        post = TestProfiledCoding(
            id=1,
            coding={}
        )

        session.execute("""
            CREATE TABLE test_coding (
                id INTEGER, coding fhir_coding);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('Field code in column fhir_coding not '
                'nullable') in str(excinfo.value)
        assert ('Field display in column fhir_coding not '
                'nullable') in str(excinfo.value)
        assert ('Field system in column fhir_coding not '
                'nullable') in str(excinfo.value)
        assert ('Field userSelected in column fhir_coding not '
                'nullable') in str(excinfo.value)
        assert ('Field version in column fhir_coding not '
                'nullable') in str(excinfo.value)
