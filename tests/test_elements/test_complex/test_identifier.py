import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.identifier import (
    IdentifierField, Identifier as IdentifierDef)


class TestIdentifier(object):

    @pytest.fixture
    def TestIdentifierModel(self, Base):
        class TestIdentifierModel(Base):
            __tablename__ = 'test_identifier'
            id = Column(primitives.IntegerField, primary_key=True)
            identifier = Column(IdentifierField())
        return TestIdentifierModel

    def test_post_data(self, session, TestIdentifierModel):
        post = TestIdentifierModel(
            id=1,
            identifier={
                "system": "system",
                "use": "secondary",
                "value": "value",
                "assigner": {
                    "reference": "reference url",
                    "display": "Patient X"
                },
                "type": {
                    "text": "text",
                    "coding": [
                        {
                            "code": "UDI",
                            "display": "display",
                            "system": "http://testing.test.com",
                            "userSelected": True,
                            "version": "2.3"
                        }]
                },
                "period": {
                    "start": "2011-05-24",
                    "end": "2011-06-24"
                }
            }
        )

        session.execute("""
            CREATE TABLE test_identifier (
                id INTEGER, identifier fhir_identifier);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestIdentifierModel).first()
        assert get.id == 1
        assert get.identifier.assigner.display == 'Patient X'

    def test_post_data_with_use_not_in_valuesets(
            self, session, TestIdentifierModel):
        post = TestIdentifierModel(
            id=1,
            identifier={
                'system': 'system',
                'use': 'uongo',
                'value': 'value',
                'assigner': {
                    'reference': 'reference url',
                    'display': 'Patient X'
                },
                'type': {
                    'text': 'text',
                    'coding': [
                        {
                            'code': 'UDI',
                            'display': 'display',
                            'system': 'http://testing.test.com',
                            'userSelected': True,
                            'version': '2.3'
                        }]
                },
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_identifier (
                id INTEGER, identifier fhir_identifier);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'The identifier use must be defined in' in str(excinfo.value)

    def test_post_data_with_type_code_not_in_valuesets(
            self, session, TestIdentifierModel):
        post = TestIdentifierModel(
            id=1,
            identifier={
                'system': 'system',
                'use': 'official',
                'value': 'value',
                'assigner': {
                    'reference': 'reference url',
                    'display': 'Patient X'
                },
                'type': {
                    'text': 'text',
                    'coding': [
                        {
                            'code': 'haiko',
                            'display': 'display',
                            'system': 'http://testing.test.com',
                            'userSelected': True,
                            'version': '2.3'
                        }]
                },
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_identifier (
                id INTEGER, identifier fhir_identifier);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'The identifier type must be defined in' in str(
            excinfo.value)

    def test_reject_data_if_identifier_value_not_unique(
            self, session, TestIdentifierModel):
        post = TestIdentifierModel(
            id=1,
            identifier={
                'system': 'system',
                'use': 'official',
                'value': 'value',
                'assigner': {
                    'reference': 'reference url',
                    'display': 'Patient X'
                },
                'type': {
                    'text': 'text',
                    'coding': [
                        {
                            'code': 'haiko',
                            'display': 'display',
                            'system': 'http://testing.test.com',
                            'userSelected': True,
                            'version': '2.3'
                        }]
                },
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )
        post2 = TestIdentifierModel(
            id=1,
            identifier={
                'system': 'system',
                'use': 'official',
                'value': 'value',
                'assigner': {
                    'reference': 'reference url',
                    'display': 'Patient X'
                },
                'type': {
                    'text': 'text',
                    'coding': [
                        {
                            'code': 'haiko',
                            'display': 'display',
                            'system': 'http://testing.test.com',
                            'userSelected': True,
                            'version': '2.3'
                        }]
                },
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_identifier (
                id INTEGER, identifier fhir_identifier);""")

        session.add(post)
        session.add(post2)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'The identifier type must be defined in' in str(
            excinfo.value)

    def test_post_data_with_null_identifier_field(
            self, session, TestIdentifierModel):
        post = TestIdentifierModel(
            id=1,
            identifier={}
        )

        session.execute("""
            CREATE TABLE test_identifier (
                id INTEGER, identifier fhir_identifier);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestIdentifierModel).first()
        assert get.id == 1
        assert get.identifier.type is None

    @pytest.fixture
    def ProfiledIdentifier(self):
        class Identifier(IdentifierDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality['mini'] = 1

                return fields

        return Identifier()()

    @pytest.fixture
    def TestProfiledIdentifier(self, Base):
        class TestProfiledIdentifier(Base):
            __tablename__ = 'test_identifier'
            id = Column(primitives.IntegerField, primary_key=True)
            identifier = Column(self.ProfiledIdentifier())
        return TestProfiledIdentifier

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledIdentifier()
        system = [field for field in fields.columns if field.name == 'system']
        use = [field for field in fields.columns if field.name == 'use']
        value = [field for field in fields.columns if field.name == 'value']
        assigner = [
            field for field in fields.columns if field.name == 'assigner']
        period = [field for field in fields.columns if field.name == 'period']
        ftype = [field for field in fields.columns if field.name == 'type']

        assert not system[0].nullable
        assert not use[0].nullable
        assert not value[0].nullable
        assert not assigner[0].nullable
        assert not period[0].nullable
        assert not ftype[0].nullable

    def test_post_data_fields_present(
            self, session, TestProfiledIdentifier):
        post = TestProfiledIdentifier(
            id=1,
            identifier={
                'system': 'system',
                'use': 'secondary',
                'value': 'value',
                'assigner': {
                    'reference': 'reference url',
                    'display': 'Patient X'
                },
                'type': {
                    'text': 'text',
                    'coding': [
                        {
                            'code': 'UDI',
                            'display': 'display',
                            'system': 'http://testing.test.com',
                            'userSelected': True,
                            'version': '2.3'
                        }]
                },
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_identifier (
                id INTEGER, identifier fhir_identifier);""")

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledIdentifier).first()
        assert get.id == 1
        assert get.identifier.assigner.display == 'Patient X'

    def test_fail_to_post_data_missing_fields(
            self, session, TestProfiledIdentifier):
        post = TestProfiledIdentifier(
            id=1,
            identifier={}
        )

        session.execute("""
            CREATE TABLE test_identifier (
                id INTEGER, identifier fhir_identifier);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('Field system in column fhir_identifier not '
                'nullable') in str(excinfo.value)
        assert ('Field use in column fhir_identifier not '
                'nullable') in str(excinfo.value)
        assert ('Field value in column fhir_identifier not '
                'nullable') in str(excinfo.value)
        assert ('Field assigner in column fhir_identifier not '
                'nullable') in str(excinfo.value)
        assert ('Field period in column fhir_identifier not '
                'nullable') in str(excinfo.value)
        assert ('Field type in column fhir_identifier not '
                'nullable') in str(excinfo.value)
