from unittest.mock import patch

import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.humanname import (
    HumanNameField, HumanName as HumanNameDef)


class TestHumanName(object):

    @pytest.fixture
    def TestHumanNameModel(self, Base):
        class TestHumanNameModel(Base):
            __tablename__ = 'test_humanname'
            id = Column(primitives.IntegerField, primary_key=True)
            humanname = Column(HumanNameField())
        return TestHumanNameModel

    @patch('fhir_server.helpers.validations.requests.get')
    def test_post_data(self, mock_get, session, TestHumanNameModel):
        mock_get.return_value.json.return_value = {
            'count': 2,
            'data': [
                {'code': 'official'}
            ]}
        post = TestHumanNameModel(
            id=1,
            humanname={
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
            }
        )

        session.execute("""
            CREATE TABLE test_humanname (
                id INTEGER, humanname fhir_humanname);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestHumanNameModel).first()
        assert get.id == 1
        assert get.humanname.suffix[0] == 'suffix'

    def test_post_data_with_whitespace_on_family_fails(
            self, session, TestHumanNameModel):
        post = TestHumanNameModel(
            id=1,
            humanname={
                'family': ['fami  ly', 'family2'],
                'given': ['given', 'given2'],
                'prefix': ['prefix', 'prefix2'],
                'suffix': ['suffix', 'suffix2'],
                'text': 'family given',
                'use': 'official',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_humanname (
                id INTEGER, humanname fhir_humanname);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'family in name must not have a whitespace' in str(
            excinfo.value)

    def test_post_data_with_whitespace_on_given_fails(
            self, session, TestHumanNameModel):
        post = TestHumanNameModel(
            id=1,
            humanname={
                'family': ['family', 'family2'],
                'given': ['giv  en', 'given2'],
                'prefix': ['prefix', 'prefix2'],
                'suffix': ['suffix', 'suffix2'],
                'text': 'text',
                'use': 'official',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_humanname (
                id INTEGER, humanname fhir_humanname);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'given in name must not have a whitespace' in str(
            excinfo.value)

    def test_post_data_with_whitespace_on_prefix_fails(
            self, session, TestHumanNameModel):
        post = TestHumanNameModel(
            id=1,
            humanname={
                'family': ['family', 'family2'],
                'given': ['given', 'given2'],
                'prefix': ['pre  fix', 'prefix2'],
                'suffix': ['suffix', 'suffix2'],
                'text': 'text',
                'use': 'official',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_humanname (
                id INTEGER, humanname fhir_humanname);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'prefix in name must not have a whitespace' in str(
            excinfo.value)

    def test_post_data_with_whitespace_on_suffix_fails(
            self, session, TestHumanNameModel):
        post = TestHumanNameModel(
            id=1,
            humanname={
                'family': ['family', 'family2'],
                'given': ['given', 'given2'],
                'prefix': ['prefix', 'prefix2'],
                'suffix': ['suff  ix', 'suffix2'],
                'text': 'text',
                'use': 'official',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_humanname (
                id INTEGER, humanname fhir_humanname);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'suffix in name must not have a whitespace' in str(
            excinfo.value)

    def test_text_attributes_not_composed_of_other_name_attributes_fails(
            self, session, TestHumanNameModel):
        post = TestHumanNameModel(
            id=1,
            humanname={
                'family': ['family', 'family2'],
                'given': ['given', 'given2'],
                'prefix': ['prefix', 'prefix2'],
                'suffix': ['suffix', 'suffix2'],
                'text': 'text',
                'use': 'official',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_humanname (
                id INTEGER, humanname fhir_humanname);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'text must be composed of the other name attributes' in str(
            excinfo.value)

    @patch('fhir_server.helpers.validations.requests.get')
    def test_post_data_with_use_not_defined_in_valuesets(
            self, mock_get, session, TestHumanNameModel):
        mock_get.return_value.json.return_value = {
            'count': 2,
            'data': [
                {'code': '<'}
            ]}
        post = TestHumanNameModel(
            id=1,
            humanname={
                'family': ['family', 'family2'],
                'given': ['given', 'given2'],
                'prefix': ['prefix', 'prefix2'],
                'suffix': ['suffix', 'suffix2'],
                'text': 'family given',
                'use': 'officialyaglar',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_humanname (
                id INTEGER, humanname fhir_humanname);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'The humanname use must be defined in' in str(
            excinfo.value)

    def test_post_data_with_null_humanname_field(
            self, session, TestHumanNameModel):
        post = TestHumanNameModel(
            id=1,
            humanname={}
        )

        session.execute("""
            CREATE TABLE test_humanname (
                id INTEGER, humanname fhir_humanname);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestHumanNameModel).first()
        assert get.id == 1
        assert get.humanname.family is None

    @pytest.fixture
    def ProfiledHumanName(self):
        class HumanName(HumanNameDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality['mini'] = 1

                return fields

        return HumanName()()

    @pytest.fixture
    def TestProfiledHumanName(self, Base):
        class TestProfiledHumanName(Base):
            __tablename__ = 'test_humanname'
            id = Column(primitives.IntegerField, primary_key=True)
            humanname = Column(self.ProfiledHumanName())
        return TestProfiledHumanName

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledHumanName()
        family = [field for field in fields.columns if field.name == 'family']
        given = [field for field in fields.columns if field.name == 'given']
        prefix = [field for field in fields.columns if field.name == 'prefix']
        suffix = [field for field in fields.columns if field.name == 'suffix']
        text = [field for field in fields.columns if field.name == 'text']
        use = [field for field in fields.columns if field.name == 'use']
        period = [field for field in fields.columns if field.name == 'period']

        assert not family[0].nullable
        assert not given[0].nullable
        assert not prefix[0].nullable
        assert not suffix[0].nullable
        assert not text[0].nullable
        assert not use[0].nullable
        assert not period[0].nullable

    @patch('fhir_server.helpers.validations.requests.get')
    def test_post_data_fields_present(
            self, mock_get, session, TestProfiledHumanName):
        mock_get.return_value.json.return_value = {
            'count': 1,
            'data': [
                {'code': 'official'}
            ]}
        post = TestProfiledHumanName(
            id=1,
            humanname={
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
            }
        )

        session.execute("""
            CREATE TABLE test_humanname (
                id INTEGER, humanname fhir_humanname);""")

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledHumanName).first()
        assert get.id == 1
        assert get.humanname.use == 'official'

    def test_fail_to_post_data_missing_fields(
            self, session, TestProfiledHumanName):
        post = TestProfiledHumanName(
            id=1,
            humanname={}
        )

        session.execute("""
            CREATE TABLE test_humanname (
                id INTEGER, humanname fhir_humanname);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('Field family in column fhir_humanname not '
                'nullable') in str(excinfo.value)
        assert ('Field given in column fhir_humanname not '
                'nullable') in str(excinfo.value)
        assert ('Field prefix in column fhir_humanname not '
                'nullable') in str(excinfo.value)
        assert ('Field suffix in column fhir_humanname not '
                'nullable') in str(excinfo.value)
        assert ('Field text in column fhir_humanname not '
                'nullable') in str(excinfo.value)
        assert ('Field use in column fhir_humanname not '
                'nullable') in str(excinfo.value)
        assert ('Field period in column fhir_humanname not '
                'nullable') in str(excinfo.value)
