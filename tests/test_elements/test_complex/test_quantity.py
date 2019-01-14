from unittest.mock import patch
from decimal import Decimal
import pytest
import warnings

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.quantity import (
    SimpleQuantity as SimpleQuantityDef,
    SimpleQuantityField,
    Quantity as QuantityDef,
    QuantityField,
)


class TestSimpleQuantity(object):
    @pytest.fixture
    def TestSimpleQuantityModel(self, Base):
        class TestSimpleQuantityModel(Base):
            __tablename__ = "test_simplequantity"
            id = Column(primitives.IntegerField, primary_key=True)
            simplequantity = Column(SimpleQuantityField())

        return TestSimpleQuantityModel

    @patch("fhir_server.helpers.validations.requests.get")
    def test_post_data(self, mock_get, session, TestSimpleQuantityModel):
        mock_get.return_value.json.return_value = {"count": 2, "data": [{"code": "kg"}]}
        post = TestSimpleQuantityModel(
            id=1,
            simplequantity={
                "code": "code",
                "system": "http://unitsofmeasure.org",
                "unit": "kg",
                "value": 2.400023,
            },
        )

        session.execute(
            """
            CREATE TABLE test_simplequantity (
                id INTEGER, simplequantity fhir_simplequantity);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestSimpleQuantityModel).first()
        assert get.id == 1
        assert get.simplequantity.value == Decimal("2.400023")

    @patch("fhir_server.helpers.validations.requests.get")
    def test_warning_if_system_is_not_unitsofmeasure_org(
        self, mock_get, session, TestSimpleQuantityModel
    ):
        mock_get.return_value.json.return_value = {"count": 2, "data": [{"code": "kg"}]}
        post = TestSimpleQuantityModel(
            id=1,
            simplequantity={
                "code": "code",
                "system": "http://someotheruom.org",
                "unit": "kg",
                "value": 2.400023,
            },
        )

        session.execute(
            """
            CREATE TABLE test_simplequantity (
                id INTEGER, simplequantity fhir_simplequantity);"""
        )

        session.add(post)

        register_composites(session.connection())
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            session.commit()
            assert len(w) == 1
            assert "Your are using a different unit of measure system." in str(
                w[-1].message
            )

        get = session.query(TestSimpleQuantityModel).first()
        assert get.id == 1
        assert get.simplequantity.system == "http://someotheruom.org"

    def test_post_data_with_null_simplequantity_field(
        self, session, TestSimpleQuantityModel
    ):
        post = TestSimpleQuantityModel(id=1, simplequantity={})

        session.execute(
            """
            CREATE TABLE test_simplequantity (
                id INTEGER, simplequantity fhir_simplequantity);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestSimpleQuantityModel).first()
        assert get.id == 1
        assert get.simplequantity.code is None

    @pytest.fixture
    def ProfiledSimpleQuantity(self):
        class SimpleQuantity(SimpleQuantityDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality["mini"] = 1

                return fields

        return SimpleQuantity()()

    @pytest.fixture
    def TestProfiledSimpleQuantity(self, Base):
        class TestProfiledSimpleQuantity(Base):
            __tablename__ = "test_simplequantity"
            id = Column(primitives.IntegerField, primary_key=True)
            simplequantity = Column(self.ProfiledSimpleQuantity())

        return TestProfiledSimpleQuantity

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledSimpleQuantity()
        code = [field for field in fields.columns if field.name == "code"]
        system = [field for field in fields.columns if field.name == "system"]
        unit = [field for field in fields.columns if field.name == "unit"]
        value = [field for field in fields.columns if field.name == "value"]

        assert not code[0].nullable
        assert not system[0].nullable
        assert not unit[0].nullable
        assert not value[0].nullable

    @patch("fhir_server.helpers.validations.requests.get")
    def test_post_data_fields_present(
        self, mock_get, session, TestProfiledSimpleQuantity
    ):
        mock_get.return_value.json.return_value = {"count": 2, "data": [{"code": "kg"}]}
        post = TestProfiledSimpleQuantity(
            id=1,
            simplequantity={
                "code": "code",
                "system": "http://unitsofmeasure.org",
                "unit": "kg",
                "value": 2.400023,
            },
        )

        session.execute(
            """
            CREATE TABLE test_simplequantity (
                id INTEGER, simplequantity fhir_simplequantity);"""
        )

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledSimpleQuantity).first()
        assert get.id == 1
        assert get.simplequantity.code == "code"

    def test_fail_to_post_data_missing_fields(
        self, session, TestProfiledSimpleQuantity
    ):
        post = TestProfiledSimpleQuantity(id=1, simplequantity={})

        session.execute(
            """
            CREATE TABLE test_simplequantity (
                id INTEGER, simplequantity fhir_simplequantity);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ("Field code in column fhir_simplequantity not " "nullable") in str(
            excinfo.value
        )
        assert ("Field system in column fhir_simplequantity not " "nullable") in str(
            excinfo.value
        )
        assert ("Field unit in column fhir_simplequantity not " "nullable") in str(
            excinfo.value
        )
        assert ("Field value in column fhir_simplequantity not " "nullable") in str(
            excinfo.value
        )


class TestQuantity(object):
    @pytest.fixture
    def TestQuantityModel(self, Base):
        class TestQuantityModel(Base):
            __tablename__ = "test_quantity"
            id = Column(primitives.IntegerField, primary_key=True)
            quantity = Column(QuantityField())

        return TestQuantityModel

    @patch("fhir_server.helpers.validations.requests.get")
    def test_post_data(self, mock_get, session, TestQuantityModel):
        mock_get.return_value.json.return_value = {
            "count": 2,
            "data": [{"code": "kg"}, {"code": "<"}],
        }
        post = TestQuantityModel(
            id=1,
            quantity={
                "code": "code",
                "system": "http://unitsofmeasure.org",
                "unit": "kg",
                "value": 2.400023,
                "comparator": "<",
            },
        )

        session.execute(
            """
            CREATE TABLE test_quantity (
                id INTEGER, quantity fhir_quantity);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestQuantityModel).first()
        assert get.id == 1
        assert get.quantity.value == Decimal("2.400023")

    @patch("fhir_server.helpers.validations.requests.get")
    def test_warning_if_system_is_not_unitsofmeasure_org(
        self, mock_get, session, TestQuantityModel
    ):
        mock_get.return_value.json.return_value = {
            "count": 2,
            "data": [{"code": "secondary"}],
        }
        post = TestQuantityModel(
            id=1,
            quantity={
                "code": "code",
                "system": "http://someotheruom.org",
                "unit": "kg",
                "value": 2.400023,
            },
        )

        session.execute(
            """
            CREATE TABLE test_quantity (
                id INTEGER, quantity fhir_quantity);"""
        )

        session.add(post)
        register_composites(session.connection())
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            session.commit()
            assert len(w) == 1
            assert "Your are using a different unit of measure system." in str(
                w[-1].message
            )

    def test_post_data_with_null_quantity_field(self, session, TestQuantityModel):
        post = TestQuantityModel(id=1, quantity={})

        session.execute(
            """
            CREATE TABLE test_quantity (
                id INTEGER, quantity fhir_quantity);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestQuantityModel).first()
        assert get.id == 1
        assert get.quantity.code is None

    @patch("fhir_server.helpers.validations.requests.get")
    def test_post_fail_if_comparator_not_present_in_valueset(
        self, mock_get, session, TestQuantityModel
    ):
        mock_get.return_value.json.return_value = {
            "count": 2,
            "data": [{"code": "secondary"}],
        }
        post = TestQuantityModel(
            id=1,
            quantity={
                "code": "code",
                "system": "http://unitsofmeasure.org",
                "unit": "kg",
                "value": 2.400023,
                "comparator": "!=",
            },
        )

        session.execute(
            """
            CREATE TABLE test_quantity (
                id INTEGER, quantity fhir_quantity);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert "The quantity comparator must be defined in" in str(excinfo.value)

    @patch("fhir_server.helpers.validations.requests.get")
    def test_post_fail_if_code_present_and_no_system(
        self, mock_get, session, TestQuantityModel
    ):
        mock_get.return_value.json.return_value = {
            "count": 2,
            "data": [{"code": "secondary"}, {"code": "<"}],
        }
        post = TestQuantityModel(
            id=1,
            quantity={
                "code": "code",
                "unit": "kg",
                "value": 2.400023,
                "comparator": "<",
            },
        )

        session.execute(
            """
            CREATE TABLE test_quantity (
                id INTEGER, quantity fhir_quantity);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert "system must be specified if code is provided" in str(excinfo.value)

    @pytest.fixture
    def ProfiledQuantity(self):
        class Quantity(QuantityDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality["mini"] = 1

                return fields

        return Quantity()()

    @pytest.fixture
    def TestProfiledQuantity(self, Base):
        class TestProfiledQuantity(Base):
            __tablename__ = "test_quantity"
            id = Column(primitives.IntegerField, primary_key=True)
            quantity = Column(self.ProfiledQuantity())

        return TestProfiledQuantity

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledQuantity()
        code = [field for field in fields.columns if field.name == "code"]
        system = [field for field in fields.columns if field.name == "system"]
        unit = [field for field in fields.columns if field.name == "unit"]
        value = [field for field in fields.columns if field.name == "value"]
        comparator = [field for field in fields.columns if field.name == "comparator"]

        assert not code[0].nullable
        assert not system[0].nullable
        assert not unit[0].nullable
        assert not value[0].nullable
        assert not comparator[0].nullable

    @patch("fhir_server.helpers.validations.requests.get")
    def test_post_data_fields_present(self, mock_get, session, TestProfiledQuantity):
        mock_get.return_value.json.return_value = {
            "count": 2,
            "data": [{"code": "kg"}, {"code": "<"}],
        }
        post = TestProfiledQuantity(
            id=1,
            quantity={
                "code": "code",
                "system": "http://unitsofmeasure.org",
                "unit": "kg",
                "value": 2.400023,
                "comparator": "<",
            },
        )

        session.execute(
            """
            CREATE TABLE test_quantity (
                id INTEGER, quantity fhir_quantity);"""
        )

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledQuantity).first()
        assert get.id == 1
        assert get.quantity.code == "code"

    def test_fail_to_post_data_missing_fields(self, session, TestProfiledQuantity):
        post = TestProfiledQuantity(id=1, quantity={})

        session.execute(
            """
            CREATE TABLE test_quantity (
                id INTEGER, quantity fhir_quantity);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ("Field code in column fhir_quantity not " "nullable") in str(
            excinfo.value
        )
        assert ("Field system in column fhir_quantity not " "nullable") in str(
            excinfo.value
        )
        assert ("Field unit in column fhir_quantity not " "nullable") in str(
            excinfo.value
        )
        assert ("Field value in column fhir_quantity not " "nullable") in str(
            excinfo.value
        )
        assert ("Field comparator in column fhir_quantity not " "nullable") in str(
            excinfo.value
        )
