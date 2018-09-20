import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.resources.identification.organization import (
    OrganizationContactField,
    OrganizationContact as OrganizationContactDef)


class TestOrganizationContact(object):

    @pytest.fixture
    def TestOrganizationContactModel(self, Base):
        class TestOrganizationContactModel(Base):
            __tablename__ = 'test_organizationcontact'
            id = Column(primitives.IntegerField, primary_key=True)
            organizationcontact = Column(OrganizationContactField())
        return TestOrganizationContactModel

    def test_post_data(self, session, TestOrganizationContactModel):
        post = TestOrganizationContactModel(
            id=1,
            organizationcontact={
                'purpose': {
                    'text': 'text',
                    'coding': [
                        {
                            'code': 'BILL',
                            'display': 'display',
                            'system': 'http://testing.test.com',
                            'userSelected': True,
                            'version': '2.3'
                        }]
                },
                'name': {
                    'family': ['family', 'family2'],
                    'given': ['given', 'given2'],
                    'prefix': ['prefix', 'prefix2'],
                    'suffix': ['suffix', 'suffix2'],
                    'text': 'family given',
                    'use': 'official',
                    'period': {
                        'start': '2011-05-24',
                        'end': '2011-06-24'
                    }
                },
                'address': {
                    'use': 'home',
                    'text': 'text',
                    'type': 'postal',
                    'state': 'state',
                    'postalCode': 'postal code',
                    'line': ['line1', 'line2'],
                    'district': 'district',
                    'country': 'country',
                    'city': 'city',
                    'period': {
                        'start': '2011-05-24',
                        'end': '2011-06-24'
                    }
                },
                'telecom': [
                    {
                        'rank': 2,
                        'system': 'phone',
                        'use': 'home',
                        'value': '+254712122988',
                        'period': {
                            'start': '2011-05-24',
                            'end': '2011-06-24'
                        }
                    }
                ]
            }
        )

        session.execute("""
            CREATE TABLE test_organizationcontact (
                id INTEGER, organizationcontact fhir_organizationcontact);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestOrganizationContactModel).first()
        assert get.id == 1
        assert get.organizationcontact.name.use == 'official'
        assert get.organizationcontact.telecom[0].rank == 2
        assert get.organizationcontact.address.use == 'home'

    def test_reject_data_with_purpose_code_no_in_valuesets(
            self, session, TestOrganizationContactModel):
        post = TestOrganizationContactModel(
            id=1,
            organizationcontact={
                'purpose': {
                    'text': 'text',
                    'coding': [
                        {
                            'code': 'NO-TRUE',
                            'display': 'display',
                            'system': 'http://testing.test.com',
                            'userSelected': True,
                            'version': '2.3'
                        }]
                },
                'name': {
                    'family': ['family', 'family2'],
                    'given': ['given', 'given2'],
                    'prefix': ['prefix', 'prefix2'],
                    'suffix': ['suffix', 'suffix2'],
                    'text': 'family given',
                    'use': 'official',
                    'period': {
                        'start': '2011-05-24',
                        'end': '2011-06-24'
                    }
                },
                'address': {
                    'use': 'home',
                    'text': 'text',
                    'type': 'postal',
                    'state': 'state',
                    'postalCode': 'postal code',
                    'line': ['line1', 'line2'],
                    'district': 'district',
                    'country': 'country',
                    'city': 'city',
                    'period': {
                        'start': '2011-05-24',
                        'end': '2011-06-24'
                    }
                },
                'telecom': [
                    {
                        'rank': 2,
                        'system': 'phone',
                        'use': 'home',
                        'value': '+254712122988',
                        'period': {
                            'start': '2011-05-24',
                            'end': '2011-06-24'
                        }
                    }
                ]
            }
        )

        session.execute("""
            CREATE TABLE test_organizationcontact (
                id INTEGER, organizationcontact fhir_organizationcontact);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('The organization contact type must be defined in') in str(
            excinfo.value)

    @pytest.fixture
    def ProfiledOrganizationContact(self):
        class OrganizationContact(OrganizationContactDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality['mini'] = 1

                return fields

        return OrganizationContact()()

    @pytest.fixture
    def TestProfiledOrganizationContact(self, Base):
        class TestProfiledOrganizationContact(Base):
            __tablename__ = 'test_organizationcontact'
            id = Column(primitives.IntegerField, primary_key=True)
            organizationcontact = Column(self.ProfiledOrganizationContact())
        return TestProfiledOrganizationContact

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledOrganizationContact()
        purpose = [field for field in fields.columns if field.name == 'purpose']
        name = [field for field in fields.columns if field.name == 'name']
        address = [field for field in fields.columns if field.name == 'address']
        telecom = [field for field in fields.columns if field.name == 'telecom']

        assert not purpose[0].nullable
        assert not name[0].nullable
        assert not address[0].nullable
        assert not telecom[0].nullable

    def test_post_data_fields_present(
            self, session, TestProfiledOrganizationContact):
        post = TestProfiledOrganizationContact(
            id=1,
            organizationcontact={
                'purpose': {
                    'text': 'text',
                    'coding': [
                        {
                            'code': 'BILL',
                            'display': 'display',
                            'system': 'http://testing.test.com',
                            'userSelected': True,
                            'version': '2.3'
                        }]
                },
                'name': {
                    'family': ['family', 'family2'],
                    'given': ['given', 'given2'],
                    'prefix': ['prefix', 'prefix2'],
                    'suffix': ['suffix', 'suffix2'],
                    'text': 'family given',
                    'use': 'official',
                    'period': {
                        'start': '2011-05-24',
                        'end': '2011-06-24'
                    }
                },
                'address': {
                    'use': 'home',
                    'text': 'text',
                    'type': 'postal',
                    'state': 'state',
                    'postalCode': 'postal code',
                    'line': ['line1', 'line2'],
                    'district': 'district',
                    'country': 'country',
                    'city': 'city',
                    'period': {
                        'start': '2011-05-24',
                        'end': '2011-06-24'
                    }
                },
                'telecom': [
                    {
                        'rank': 2,
                        'system': 'phone',
                        'use': 'home',
                        'value': '+254712122988',
                        'period': {
                            'start': '2011-05-24',
                            'end': '2011-06-24'
                        }
                    }
                ],
                'modifierExtension': None
            }
        )

        session.execute("""
            CREATE TABLE test_organizationcontact (
                id INTEGER, organizationcontact fhir_organizationcontact);""")

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledOrganizationContact).first()
        assert get.id == 1
        assert get.organizationcontact.name.use == 'official'

    def test_fail_to_post_data_missing_fields(
            self, session, TestProfiledOrganizationContact):
        post = TestProfiledOrganizationContact(
            id=1,
            organizationcontact={}
        )

        session.execute("""
            CREATE TABLE test_organizationcontact (
                id INTEGER, organizationcontact fhir_organizationcontact);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('Field purpose in column fhir_organizationcontact not '
                'nullable') in str(excinfo.value)
        assert ('Field name in column fhir_organizationcontact not '
                'nullable') in str(excinfo.value)
        assert ('Field telecom in column fhir_organizationcontact not '
                'nullable') in str(excinfo.value)
        assert ('Field address in column fhir_organizationcontact not '
                'nullable') in str(excinfo.value)
