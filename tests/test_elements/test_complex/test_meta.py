import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.meta import MetaField, Meta as MetaDef


class TestMeta(object):
    @pytest.fixture
    def TestMetaModel(self, Base):
        class TestMetaModel(Base):
            __tablename__ = "test_meta"
            id = Column(primitives.IntegerField, primary_key=True)
            meta = Column(MetaField(), nullable=False)

        return TestMetaModel

    def test_post_data(self, session, TestMetaModel):
        post = TestMetaModel(
            id=1,
            meta={
                "versionId": "1.2a23",
                "lastUpdated": "2011-05-24T10:10:10+0300",
                "profile": [
                    "http://example.com/fhir/Patient/",
                    "http://example.com/fhir/Organization/",
                ],
                "security": [
                    {
                        "code": "dkls323-3223hj",
                        "display": "display",
                        "system": "http://example.com/fhir/Security/",
                        "userSelected": True,
                        "version": "2.3",
                    }
                ],
                "tag": [
                    {
                        "code": "dkls323-3223hj",
                        "display": "display",
                        "system": "http://example.com/fhir/tag/",
                        "userSelected": True,
                        "version": "2.3",
                    }
                ],
            },
        )

        session.execute(
            """
            CREATE TABLE test_meta (
                id INTEGER, meta fhir_meta);"""
        )

        register_composites(session.connection())
        session.add(post)
        session.commit()
        get = session.query(TestMetaModel).first()
        assert get.id == 1
        assert str(get.meta.versionId) == "1.2a23"

    def test_post_data_with_null_meta_field(self, session, TestMetaModel):
        post = TestMetaModel(id=1, meta={})

        session.execute(
            """
            CREATE TABLE test_meta (
                id INTEGER, meta fhir_meta);"""
        )

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestMetaModel).first()
        assert get.id == 1
        assert get.meta.versionId is None

    @pytest.fixture
    def ProfiledMeta(self):
        class Meta(MetaDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    field.cardinality["mini"] = 1

                return fields

        return Meta()()

    @pytest.fixture
    def TestProfiledMeta(self, Base):
        class TestProfiledMeta(Base):
            __tablename__ = "test_meta"
            id = Column(primitives.IntegerField, primary_key=True)
            meta = Column(self.ProfiledMeta())

        return TestProfiledMeta

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledMeta()
        versionId = [field for field in fields.columns if field.name == "versionId"]
        lastUpdated = [field for field in fields.columns if field.name == "lastUpdated"]
        profile = [field for field in fields.columns if field.name == "profile"]
        security = [field for field in fields.columns if field.name == "security"]
        tag = [field for field in fields.columns if field.name == "tag"]

        assert not versionId[0].nullable
        assert not lastUpdated[0].nullable
        assert not profile[0].nullable
        assert not security[0].nullable
        assert not tag[0].nullable

    def test_post_data_fields_present(self, session, TestProfiledMeta):
        post = TestProfiledMeta(
            id=1,
            meta={
                "versionId": "1.2a23",
                "lastUpdated": "2011-05-24T10:10:10+0300",
                "profile": [
                    "http://example.com/fhir/Patient/",
                    "http://example.com/fhir/Organization/",
                ],
                "security": [
                    {
                        "code": "dkls323-3223hj",
                        "display": "display",
                        "system": "http://example.com/fhir/Security/",
                        "userSelected": True,
                        "version": "2.3",
                    }
                ],
                "tag": [
                    {
                        "code": "dkls323-3223hj",
                        "display": "display",
                        "system": "http://example.com/fhir/tag/",
                        "userSelected": True,
                        "version": "2.3",
                    }
                ],
            },
        )

        session.execute(
            """
            CREATE TABLE test_meta (
                id INTEGER, meta fhir_meta);"""
        )

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledMeta).first()
        assert get.id == 1
        assert str(get.meta.versionId) == "1.2a23"

    def test_fail_to_post_data_missing_fields(self, session, TestProfiledMeta):
        post = TestProfiledMeta(id=1, meta={})

        session.execute(
            """
            CREATE TABLE test_meta (
                id INTEGER, meta fhir_meta);"""
        )

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()

        assert "Field versionId in column fhir_meta not nullable" in str(excinfo.value)
        assert "Field lastUpdated in column fhir_meta not nullable" in str(
            excinfo.value
        )
        assert "Field profile in column fhir_meta not nullable" in str(excinfo.value)
        assert "Field security in column fhir_meta not nullable" in str(excinfo.value)
        assert "Field tag in column fhir_meta not nullable" in str(excinfo.value)
