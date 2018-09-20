import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements.opentype import OpenType
from fhir_server.elements import primitives
from fhir_server.elements.extension import (
    ElementExtension, Extension as ExtensionDef)


def test_opentype_coerced():
    assert OpenType.coerce_compared_value(
        OpenType(), '=', {'key': 'value'})


class TestExtensions(object):

    @pytest.fixture
    def TestExtensionModel(self, Base):
        class TestExtensionModel(Base):
            __tablename__ = 'test_extension'
            id = Column(primitives.IntegerField, primary_key=True)
            extension = Column(ElementExtension(), nullable=False)
        return TestExtensionModel

    def test_post_data(self, session, TestExtensionModel):
        post = TestExtensionModel(
            id=1,
            extension={
                'url': 'http://hl7.org/fhir/extensions',
                'value': {'valueString': 'string val'}
            }
        )

        post2 = TestExtensionModel(
            id=2,
            extension=None
        )

        session.execute("""
            CREATE TABLE test_extension (
                id INTEGER, extension fhir_extension);""")

        register_composites(session.connection())
        session.add(post)
        session.add(post2)
        session.commit()
        get = session.query(TestExtensionModel).first()
        assert get.id == 1
        assert str(get.extension.url) == 'http://hl7.org/fhir/extensions'

    def test_post_data_with_extension_as_none(
            self, session, TestExtensionModel):

        post2 = TestExtensionModel(
            id=2,
            extension={
                'url': 'http://hl7.org/fhir/extensions',
                'value': None
            }
        )

        session.execute("""
            CREATE TABLE test_extension (
                id INTEGER, extension fhir_extension);""")

        register_composites(session.connection())
        session.add(post2)
        session.commit()
        get = session.query(TestExtensionModel).first()
        assert get.id == 2

    def test_reject_invalid_data(self, session, TestExtensionModel):
        post = TestExtensionModel(
            id=1,
            extension={
                'url': 'http://hl7.org/fhir/extensions',
                'value': {'valueGuessType': 'string val'}
            }
        )

        session.execute("""
            CREATE TABLE test_extension (
                id INTEGER, extension fhir_extension);""")

        with pytest.raises(StatementError) as excinfo:
            session.add(post)
            session.commit()

        assert ("The data provided for the extensions field is "
                "invalid") in str(excinfo.value)

    @pytest.fixture
    def ProfiledExtension(self):
        class Extension(ExtensionDef):
            for ex in ExtensionDef()().columns:
                ex.nullable = False
        return Extension()()

    @pytest.fixture
    def TestProfiledExtension(self, Base):
        class TestProfiledExtension(Base):
            __tablename__ = 'test_extension'
            id = Column(primitives.IntegerField, primary_key=True)
            extension = Column(self.ProfiledExtension())
        return TestProfiledExtension

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledExtension()
        value = [
            field for field in fields.columns if field.name == 'value']

        assert value[0].nullable

    def test_post_data_fields_present(
            self, session, TestProfiledExtension):
        post = TestProfiledExtension(
            id=1,
            extension={
                'url': 'http://hl7.org/fhir/extensions',
                'value': {'valueString': 'string val'}
            }
        )

        session.execute("""
            CREATE TABLE test_extension (
                id INTEGER, extension fhir_extension);""")

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledExtension).first()
        assert get.id == 1
        assert str(get.extension.url) == 'http://hl7.org/fhir/extensions'

    def test_fail_to_post_data_missing_fields(
            self, session, TestProfiledExtension):
        post = TestProfiledExtension(
            id=1,
            extension={}
        )

        session.execute("""
            CREATE TABLE test_extension (
                id INTEGER, extension fhir_extension);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('Field url in column fhir_extension not '
                'nullable') in str(excinfo.value)
