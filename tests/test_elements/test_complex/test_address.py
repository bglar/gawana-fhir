import pytest
import warnings

from sqlalchemy import Column
from sqlalchemy_utils import register_composites
from sqlalchemy.exc import StatementError

from fhir_server.elements import primitives
from fhir_server.elements.complex.address import (
    AddressField, Address as AddressDef)


class TestAddress(object):

    @pytest.fixture
    def TestAddressModel(self, Base):
        class TestAddressModel(Base):
            __tablename__ = 'test_address'
            id = Column(primitives.IntegerField, primary_key=True)
            address = Column(AddressField())
        return TestAddressModel

    def test_save_data(self, session, TestAddressModel):
        post = TestAddressModel(
            id=1,
            address={
                "use": "home",
                "text": "text",
                "type": "postal",
                "state": "state",
                "postalCode": "postal code",
                "line": ["line1", "line2"],
                "district": "district",
                "country": "KEN",
                "city": "city",
                "period": {
                    "start": "2011-05-24",
                    "end": "2011-06-24"
                }
            }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestAddressModel).first()
        assert get.id == 1
        assert get.address.district == 'district'

    def test_post_null_data_for_address_fields(
            self, session, TestAddressModel):
        post = TestAddressModel(
            id=1,
            address={}
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestAddressModel).first()
        assert get.id == 1
        assert get.address.district is None

    def test_post_data_with_use_not_in_valueset(
            self, session, TestAddressModel):
        post = TestAddressModel(
            id=1,
            address={
                'use': 'tulia',
                'text': 'text',
                'type': 'postal',
                'state': 'state',
                'postalCode': 'postal code',
                'line': ['line1', 'line2'],
                'district': 'district',
                'country': 'KEN',
                'city': 'city',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'The address use must be defined in' in str(
            excinfo.value)

    def test_post_data_with_type_not_in_valueset(
            self, session, TestAddressModel):
        post = TestAddressModel(
            id=1,
            address={
                'use': 'home',
                'text': 'text',
                'type': 'postalyangu',
                'state': 'state',
                'postalCode': 'postal code',
                'line': ['line1', 'line2'],
                'district': 'district',
                'country': 'KEN',
                'city': 'city',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'The address type must be defined in' in str(
            excinfo.value)

    def test_warning_if_country_value_not_valid_alpha3_ISO1366(
            self, session, TestAddressModel):
        post = TestAddressModel(
            id=1,
            address={
                'use': 'home',
                'text': 'text',
                'type': 'postal',
                'state': 'state',
                'postalCode': 'postal code',
                'line': ['line1', 'line2'],
                'district': 'district',
                'country': 'AYU',
                'city': 'city',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            session.commit()
            assert len(w) == 1
            assert 'This country code is not recommended.' in str(
                w[-1].message)

    @pytest.fixture
    def ProfiledAddress(self):
        class Address(AddressDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    if field.name == 'city':
                        field.cardinality['mini'] = 1
                    if field.name == 'district':
                        field.cardinality['mini'] = 1
                    if field.name == 'country':
                        field.cardinality['mini'] = 1
                    if field.name == 'line':
                        field.cardinality['mini'] = 1
                    if field.name == 'postalCode':
                        field.cardinality['mini'] = 1
                    if field.name == 'state':
                        field.cardinality['mini'] = 1
                    if field.name == 'type':
                        field.cardinality['mini'] = 1
                    if field.name == 'text':
                        field.cardinality['mini'] = 1
                    if field.name == 'use':
                        field.cardinality['mini'] = 1
                    if field.name == 'period':
                        field.cardinality['mini'] = 1
                return fields

        return Address()()

    @pytest.fixture
    def TestProfiledAddress(self, Base):
        class TestProfiledAddress(Base):
            __tablename__ = 'test_address'
            id = Column(primitives.IntegerField, primary_key=True)
            address = Column(self.ProfiledAddress())
        return TestProfiledAddress

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledAddress()
        country = [field for field in fields.columns if field.name == 'country']
        city = [field for field in fields.columns if field.name == 'city']
        district = [
            field for field in fields.columns if field.name == 'district']
        line = [field for field in fields.columns if field.name == 'line']
        postalCode = [
            field for field in fields.columns if field.name == 'postalCode']
        state = [field for field in fields.columns if field.name == 'state']
        stype = [field for field in fields.columns if field.name == 'type']
        text = [field for field in fields.columns if field.name == 'text']
        use = [field for field in fields.columns if field.name == 'use']
        period = [field for field in fields.columns if field.name == 'period']

        assert not city[0].nullable
        assert not stype[0].nullable
        assert not district[0].nullable
        assert not country[0].nullable
        assert not line[0].nullable
        assert not postalCode[0].nullable
        assert not state[0].nullable
        assert not use[0].nullable
        assert not period[0].nullable
        assert not text[0].nullable

    def test_post_data_field_city_present(self, session, TestProfiledAddress):
        post = TestProfiledAddress(
            id=1,
            # address={
            #     'use': 'home',
            #     'text': 'text',
            #     'type': 'postal',
            #     'state': 'state',
            #     'postalCode': 'postal code',
            #     'line': ['line1', 'line2'],
            #     'district': 'district',
            #     'country': 'KEN',
            #     'city': 'city',
            #     'period': {
            #         'start': '2011-05-24',
            #         'end': '2011-06-24'
            #     }
            # }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledAddress).first()
        assert get.id == 1
        assert get.address.district == 'district'

    def test_fail_to_post_data_missing_city(self, session, TestProfiledAddress):
        post = TestProfiledAddress(
            id=1,
            address={
                'state': 'state',
                'postalCode': 'postal code',
                'line': ['line1', 'line2'],
                'country': 'KEN',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'Field city in column fhir_address not nullable' in str(
            excinfo.value)
        assert 'Field district in column fhir_address not nullable' in str(
            excinfo.value)
        assert 'Field use in column fhir_address not nullable' in str(
            excinfo.value)
        assert 'Field text in column fhir_address not nullable' in str(
            excinfo.value)
        assert 'Field type in column fhir_address not nullable' in str(
            excinfo.value)

    def test_fail_to_post_data_missing_country(
            self, session, TestProfiledAddress):
        post = TestProfiledAddress(
            id=1,
            address={
                'use': 'use',
                'text': 'text',
                'type': 'postal',
                'state': 'state',
                'postalCode': 'postal code',
                'line': ['line1', 'line2'],
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'Field country in column fhir_address not nullable' in str(
            excinfo.value)

    def test_fail_to_post_data_missing_district(
            self, session, TestProfiledAddress):
        post = TestProfiledAddress(
            id=1,
            address={
                'use': 'home',
                'text': 'text',
                'type': 'postal',
                'state': 'state',
                'postalCode': 'postal code',
                'line': ['line1', 'line2'],
                'country': 'KEN',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'Field district in column fhir_address not nullable' in str(
            excinfo.value)

    def test_fail_to_post_data_missing_line(self, session, TestProfiledAddress):
        post = TestProfiledAddress(
            id=1,
            address={
                'use': 'home',
                'text': 'text',
                'type': 'postal',
                'state': 'state',
                'postalCode': 'postal code',
                'country': 'KEN',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'Field line in column fhir_address not nullable' in str(
            excinfo.value)

    def test_fail_to_post_data_missing_postalCode(
            self, session, TestProfiledAddress):
        post = TestProfiledAddress(
            id=1,
            address={
                'use': 'home',
                'text': 'text',
                'type': 'postal',
                'state': 'state',
                'line': ['line1', 'line2'],
                'country': 'KEN',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'Field postalCode in column fhir_address not nullable' in str(
            excinfo.value)

    def test_fail_to_post_data_missing_state(
            self, session, TestProfiledAddress):
        post = TestProfiledAddress(
            id=1,
            address={
                'use': 'home',
                'text': 'text',
                'type': 'postal',
                'postalCode': 'postal code',
                'line': ['line1', 'line2'],
                'country': 'KEN',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'Field state in column fhir_address not nullable' in str(
            excinfo.value)

    def test_fail_to_post_data_missing_type(self, session, TestProfiledAddress):
        post = TestProfiledAddress(
            id=1,
            address={
                'use': 'home',
                'text': 'text',
                'state': 'state',
                'postalCode': 'postal code',
                'line': ['line1', 'line2'],
                'country': 'KEN',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'Field type in column fhir_address not nullable' in str(
            excinfo.value)

    def test_fail_to_post_data_missing_text(self, session, TestProfiledAddress):
        post = TestProfiledAddress(
            id=1,
            address={
                'use': 'home',
                'type': 'postal',
                'state': 'state',
                'postalCode': 'postal code',
                'line': ['line1', 'line2'],
                'country': 'KEN',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'Field text in column fhir_address not nullable' in str(
            excinfo.value)

    def test_fail_to_post_data_missing_use(self, session, TestProfiledAddress):
        post = TestProfiledAddress(
            id=1,
            address={
                'text': 'text',
                'type': 'postal',
                'state': 'state',
                'postalCode': 'postal code',
                'line': ['line1', 'line2'],
                'country': 'KEN',
                'period': {
                    'start': '2011-05-24',
                    'end': '2011-06-24'
                }
            }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'Field use in column fhir_address not nullable' in str(
            excinfo.value)

    def test_fail_to_post_data_missing_period(
            self, session, TestProfiledAddress):
        post = TestProfiledAddress(
            id=1,
            address={
                'use': 'home',
                'text': 'text',
                'type': 'postal',
                'state': 'state',
                'postalCode': 'postal code',
                'line': ['line1', 'line2'],
                'district': 'district',
                'country': 'KEN',
                'city': 'city'
            }
        )

        session.execute("""
            CREATE TABLE test_address (
                id INTEGER, address fhir_address);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'Field period in column fhir_address not nullable' in str(
            excinfo.value)
