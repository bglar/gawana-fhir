import uuid
import math
from decimal import Decimal
import pytest
from sqlalchemy.exc import StatementError
from sqlalchemy import Column
from fhir_server.elements import primitives


class TestDecimalField(object):
    def test_decimal_accepts_none_as_value(self):
        result = primitives.DecimalField().process_bind_param(None, "postgres")
        assert result is None

    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = "circle_test"
            id = Column(primitives.IdField, primary_key=True)
            decimal_field = Column(primitives.DecimalField)
            decimal_precison = Column(primitives.DecimalField(5, 2))

        session.execute(
            """
            CREATE TABLE circle_test (
                id TEXT, decimal_field decimal,
                decimal_precison decimal(5, 2));"""
        )

        return TestDataTypesModel

    def test_supports_arbitrary_precision(self, session, TestDataTypesModel):
        a = 1 / 3
        id = str(uuid.uuid4())
        post_data = TestDataTypesModel(id=id, decimal_field=a, decimal_precison=a)

        session.add(post_data)
        session.commit()
        get_data = session.query(TestDataTypesModel).first()
        assert get_data.decimal_precison == Decimal("0.33")

    def test_large_decimal(self, session, TestDataTypesModel):
        a = math.pow(2.0, 64) + math.pow(2, -32)
        id = str(uuid.uuid4())
        post_data = TestDataTypesModel(
            id=id, decimal_field=str(a), decimal_precison=10.0
        )

        session.add(post_data)
        session.commit()
        get_data = session.query(TestDataTypesModel).first()
        assert get_data.decimal_field == Decimal(str(a))

    def test_large_scale(self, session, TestDataTypesModel):
        a = "123444.099372825511142526188166277617938391899378736376700006828"
        id = str(uuid.uuid4())
        post_data = TestDataTypesModel(id=id, decimal_field=a, decimal_precison=10.0)

        session.add(post_data)
        session.commit()
        get_data = session.query(TestDataTypesModel).first()
        assert get_data.decimal_field == Decimal(a)

    def test_large_precision(self, session, TestDataTypesModel):
        a = "948884737366363773883123444.0993728255111425261881662776179383"
        id = str(uuid.uuid4())
        post_data = TestDataTypesModel(id=id, decimal_field=a, decimal_precison=10.0)

        session.add(post_data)
        session.commit()
        get_data = session.query(TestDataTypesModel).first()
        assert get_data.decimal_field == Decimal(a)

    def test_fail_on_passing_invalid_string_characters(
        self, session, TestDataTypesModel
    ):
        a = "948884737366363773883123444.0993728255111425261881jkhkjahdjhsj"
        id = str(uuid.uuid4())
        post_data = TestDataTypesModel(id=id, decimal_field=a, decimal_precison=10.0)

        with pytest.raises(StatementError) as err:
            session.add(post_data)
            session.commit()

        assert ("Invalid literal for Decimal:") in str(err.value)
