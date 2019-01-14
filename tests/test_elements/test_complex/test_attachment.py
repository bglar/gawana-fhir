import uuid
import pytest
import hashlib

from sqlalchemy import Column
from sqlalchemy.exc import StatementError

from sqlalchemy_utils import register_composites
from fhir_server.elements import primitives
from fhir_server.elements.complex.attachment import (
    AttachmentField,
    Attachment as AttachmentDef,
)


class TestAttachment(object):
    @pytest.fixture
    def TestAttachmentModel(self, Base):
        class TestAttachmentModel(Base):
            __tablename__ = "test_attachment"
            id = Column(primitives.IntegerField, primary_key=True)
            attachment = Column(AttachmentField())

        return TestAttachmentModel

    def test_post_data(self, session, TestAttachmentModel):
        data = "data to be encoded"
        byte_data = b"data to be encoded"
        d_hash = hashlib.sha1(byte_data).digest()
        post = TestAttachmentModel(
            id=1,
            attachment={
                "contentType": "application/pdf",
                "creation": "2011-05-24",
                "data": data,
                "hash": d_hash,
                "language": "en",
                "size": 21,
                "title": "title",
                "url": "url",
            },
        )

        session.execute(
            """
            CREATE TABLE test_attachment (
                id INTEGER, attachment fhir_attachment);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestAttachmentModel).first()
        assert get.id == 1
        assert get.attachment.contentType == "application/pdf"

    def test_rejects_data_with_invalid_contentType(self, session, TestAttachmentModel):
        data = "data to be encoded"
        byte_data = b"data to be encoded"
        d_hash = hashlib.sha1(byte_data).digest()
        post = TestAttachmentModel(
            id=1,
            attachment={
                "contentType": "application/pgp",
                "creation": "2011-05-24",
                "data": data,
                "hash": d_hash,
                "language": "en",
                "size": 21,
                "title": "title",
                "url": "url",
            },
        )

        session.execute(
            """
            CREATE TABLE test_attachment (
                id INTEGER, attachment fhir_attachment);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert "The uploaded file type not supported" in str(excinfo.value)

    def test_post_fails_if_data_present_but_no_contentType(
        self, session, TestAttachmentModel
    ):
        post = TestAttachmentModel(
            id=1,
            attachment={
                "creation": "2011-05-24",
                "data": "data to be encoded",
                "hash": "hash to be encoded",
                "language": "en",
                "size": 21,
                "title": "title",
                "url": "url",
            },
        )

        session.execute(
            """
            CREATE TABLE test_attachment (
                id INTEGER, attachment fhir_attachment);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert "content_type must be populated if data is provided" in str(
            excinfo.value
        )

    def test_post_fails_if_language_code_provided_is_not_valid(
        self, session, TestAttachmentModel
    ):
        post = TestAttachmentModel(
            id=1,
            attachment={
                "creation": "2011-05-24",
                "data": "data to be encoded",
                "hash": "hash to be encoded",
                "language": "en-sjkjdkjs",
                "size": 21,
                "title": "title",
                "url": "url",
            },
        )

        session.execute(
            """
            CREATE TABLE test_attachment (
                id INTEGER, attachment fhir_attachment);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()

        assert "the language code must be valid" in str(excinfo.value)

    def test_post_fails_if_hash_is_not_b64_encode_sha1_of_data(
        self, session, TestAttachmentModel
    ):
        post = TestAttachmentModel(
            id=1,
            attachment={
                "creation": "2011-05-24",
                "data": "data to be encoded",
                "hash": "hash to be encoded",
                "language": "en",
                "size": 21,
                "title": "title",
                "url": "url",
            },
        )

        session.execute(
            """
            CREATE TABLE test_attachment (
                id INTEGER, attachment fhir_attachment);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()

        assert "the hash must be a base64 sha-1 hash of the data" in str(excinfo.value)

    def test_post_data_with_null_attachment_field(self, session, TestAttachmentModel):
        post = TestAttachmentModel(id=1, attachment={})

        session.execute(
            """
            CREATE TABLE test_attachment (
                id INTEGER, attachment fhir_attachment);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestAttachmentModel).first()
        assert get.id == 1
        assert get.attachment.data is None

    @pytest.fixture
    def ProfiledAttachment(self):
        class Attachment(AttachmentDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality["mini"] = 1
                return fields

        return Attachment()()

    @pytest.fixture
    def TestProfiledAttachment(self, Base):
        class TestProfiledAttachment(Base):
            __tablename__ = "test_attachment"
            id = Column(primitives.IntegerField, primary_key=True)
            attachment = Column(self.ProfiledAttachment())

        return TestProfiledAttachment

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledAttachment()
        contentType = [field for field in fields.columns if field.name == "contentType"]
        creation = [field for field in fields.columns if field.name == "creation"]
        data = [field for field in fields.columns if field.name == "data"]
        language = [field for field in fields.columns if field.name == "language"]
        fhash = [field for field in fields.columns if field.name == "hash"]
        size = [field for field in fields.columns if field.name == "size"]
        title = [field for field in fields.columns if field.name == "title"]
        url = [field for field in fields.columns if field.name == "url"]

        assert not contentType[0].nullable
        assert not creation[0].nullable
        assert not data[0].nullable
        assert not language[0].nullable
        assert not fhash[0].nullable
        assert not size[0].nullable
        assert not title[0].nullable
        assert not url[0].nullable

    def test_post_data_required_fields_present(self, session, TestProfiledAttachment):
        data = "data to be encoded"
        byte_data = b"data to be encoded"
        d_hash = hashlib.sha1(byte_data).digest()
        post = TestProfiledAttachment(
            id=1,
            attachment={
                "contentType": "application/pdf",
                "creation": "2011-05-24",
                "data": data,
                "hash": d_hash,
                "language": "en",
                "size": 21,
                "title": "title",
                "url": "url",
            },
        )

        session.execute(
            """
            CREATE TABLE test_attachment (
                id INTEGER, attachment fhir_attachment);"""
        )

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledAttachment).first()
        assert get.id == 1
        assert get.attachment.contentType == "application/pdf"

    def test_fail_to_post_data_missing_required_fields(
        self, session, TestProfiledAttachment
    ):
        post = TestProfiledAttachment(id=1, attachment={})

        session.execute(
            """
            CREATE TABLE test_attachment (
                id INTEGER, attachment fhir_attachment);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ("Field contentType in column fhir_attachment not " "nullable") in str(
            excinfo.value
        )
        assert "Field creation in column fhir_attachment not nullable" in str(
            excinfo.value
        )
        assert "Field data in column fhir_attachment not nullable" in str(excinfo.value)
        assert "Field language in column fhir_attachment not nullable" in str(
            excinfo.value
        )
        assert "Field hash in column fhir_attachment not nullable" in str(excinfo.value)
        assert "Field size in column fhir_attachment not nullable" in str(excinfo.value)
        assert "Field title in column fhir_attachment not nullable" in str(
            excinfo.value
        )
        assert "Field url in column fhir_attachment not nullable" in str(excinfo.value)
