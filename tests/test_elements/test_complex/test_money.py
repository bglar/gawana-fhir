import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.money import Money as MoneyDef


PMoneyField = MoneyDef(precision=5, scale=2)


class TestMoney(object):

    @pytest.fixture
    def TestMoneyModel(self, Base):
        class TestMoneyModel(Base):
            __tablename__ = 'test_money'
            id = Column(primitives.IntegerField, primary_key=True)
            money = Column(PMoneyField(precision='5, 2'))
        return TestMoneyModel

    def test_post_data(self, session, TestMoneyModel):
        post = TestMoneyModel(
            id=1,
            money={
                'code': 'code',
                'system': 'system',
                'unit': 'ksh',
                'value': 345.55
            }
        )

        session.execute("""
            CREATE TABLE test_money (
                id INTEGER, money fhir_money);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestMoneyModel).first()
        assert get.id == 1
        assert get.money.value == '345.55'

    def test_post_data_with_non_constrained_precision(
            self, session, TestMoneyModel):
        post = TestMoneyModel(
            id=1,
            money={
                'code': 'code',
                'system': 'system',
                'unit': 'ksh',
                'value': '2331000.00232333434343'
            }
        )

        session.execute("""
            CREATE TABLE test_money (
                id INTEGER, money fhir_money);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestMoneyModel).first()
        assert get.id == 1
        assert get.money.value == '2331000.00232333434343'

    def test_code_must_be_specified_if_value_is_present(
            self, session, TestMoneyModel):
        post = TestMoneyModel(
            id=1,
            money={
                'system': 'system',
                'unit': 'ksh',
                'value': 1000.00
            }
        )

        session.execute("""
            CREATE TABLE test_money (
                id INTEGER, money fhir_money);""")

        session.add(post)

        register_composites(session.connection())

        with pytest.raises(StatementError) as excinfo:
            session.commit()

        assert 'code must be specified if value is provided' in str(
            excinfo.value)

    def test_post_data_with_null_money_field(
            self, session, TestMoneyModel):
        post = TestMoneyModel(
            id=1,
            money={}
        )

        session.execute("""
            CREATE TABLE test_money (
                id INTEGER, money fhir_money);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestMoneyModel).first()
        assert get.id == 1
        assert get.money.code is None
