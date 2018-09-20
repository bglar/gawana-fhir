import pytest
import jwt

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites
from fhir_server.elements import primitives
from fhir_server.elements.complex.signature import SignatureField


class TestSignature(object):
    encoded = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')

    @pytest.fixture
    def TestSignatureModel(self, Base):
        class TestSignatureModel(Base):
            __tablename__ = 'test_signature'
            id = Column(primitives.IntegerField, primary_key=True)
            signature = Column(SignatureField())
        return TestSignatureModel

    def test_post_data(self, session, TestSignatureModel):
        post = TestSignatureModel(
            id=1,
            signature={
                'blob': self.encoded,
                'contentType': 'application/jwt',
                'when': '2011-05-24T11:12:00+0300',
                'whoUri': 'whoUri',
                'whoReference': {
                    'reference': 'reference url',
                    'display': 'Patient X'
                },
                'type': [{
                    'code': '1.2.840.10065.1.12.1.1',
                    'display': 'display',
                    'system': 'http://testing.test.com',
                    'userSelected': True,
                    'version': '2.3'
                }]
            }
        )

        session.execute("""
            CREATE TABLE test_signature (
                id INTEGER, signature fhir_signature);""")

        session.add(post)
        register_composites(session.connection())
        session.commit()
        get = session.query(TestSignatureModel).first()
        assert get.id == 1
        assert get.signature.whoReference.display == 'Patient X'

    def test_reject_data_with_contentType_not_valid(
            self, session, TestSignatureModel):
        post = TestSignatureModel(
            id=1,
            signature={
                'blob': self.encoded,
                'contentType': 'application/not_valid',
                'when': '2011-05-24T11:12:00+0300',
                'whoUri': 'whoUri',
                'whoReference': {
                    'reference': 'reference url',
                    'display': 'Patient X'
                },
                'type': [{
                    'code': '1.2.840.10065.1.12.1.1',
                    'display': 'display',
                    'system': 'http://testing.test.com',
                    'userSelected': True,
                    'version': '2.3'
                }]
            }
        )

        session.execute("""
            CREATE TABLE test_signature (
                id INTEGER, signature fhir_signature);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'The signature content type should be one of' in str(
            excinfo.value)

    def test_reject_invalid_jwt_blob(
            self, session, TestSignatureModel):
        post = TestSignatureModel(
            id=1,
            signature={
                'blob': 'myfalse.blob',
                'contentType': 'application/jwt',
                'when': '2011-05-24T11:12:00+0300',
                'whoUri': 'whoUri',
                'whoReference': {
                    'reference': 'reference url',
                    'display': 'Patient X'
                },
                'type': [{
                    'code': '1.2.840.10065.1.12.1.1',
                    'display': 'display',
                    'system': 'http://testing.test.com',
                    'userSelected': True,
                    'version': '2.3'
                }]
            }
        )

        session.execute("""
            CREATE TABLE test_signature (
                id INTEGER, signature fhir_signature);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert 'The blob provided is not a valid jwt encoded' in str(
            excinfo.value)

    def test_excluding_required_fields_in_post(
            self, session, TestSignatureModel):
        post = TestSignatureModel(
            id=1,
            signature={
                'contentType': 'application/jwt',
                'when': '2011-05-24T11:12:00+0300',
                'whoUri': 'whoUri',
                'whoReference': {
                    'reference': 'reference url',
                    'display': 'Patient X'
                },
                'type': [{
                    'code': '1.2.840.10065.1.12.1.1',
                    'display': 'display',
                    'system': 'http://testing.test.com',
                    'userSelected': True,
                    'version': '2.3'
                }]
            }
        )

        session.execute("""
            CREATE TABLE test_signature (
                id INTEGER, signature fhir_signature);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()

        assert ('Field blob in column fhir_signature not '
                'nullable') in str(excinfo.value)

    def test_post_data_with_type_code_not_defined_in_valueset(
            self, session, TestSignatureModel):
        post = TestSignatureModel(
            id=1,
            signature={
                'blob': self.encoded,
                'contentType': 'application/jwt',
                'when': '2011-05-24T11:12:00+0300',
                'whoUri': 'whoUri',
                'whoReference': {
                    'reference': 'reference url',
                    'display': 'Patient X'
                },
                'type': [{
                    'code': 'code haiko',
                    'display': 'display',
                    'system': 'http://testing.test.com',
                    'userSelected': True,
                    'version': '2.3'
                }]
            }
        )

        session.execute("""
            CREATE TABLE test_signature (
                id INTEGER, signature fhir_signature);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()

        assert 'The signature code must be defined in' in str(excinfo.value)
