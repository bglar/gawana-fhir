"""Unit tests illustrating usage of the ``history_meta.py``
module functions."""

import pytest
import warnings

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    select,
)
from sqlalchemy.orm import (
    clear_mappers,
    Session,
    deferred,
    relationship,
    column_property,
)
from sqlalchemy.testing import AssertsCompiledSQL, eq_, assert_raises
from sqlalchemy.testing.entities import ComparableEntity
from sqlalchemy.orm import exc as orm_exc
from sqlalchemy_utils import remove_composite_listeners

from fhir_server.utils.history_tables import Versioned, versioned_session


@pytest.fixture(scope="function")
def session1(db, request):
    """Creates a new database session for a test.

    Do not confuse this fixture for the overall session fixture in conftest.py
    The session used in `conftest.py` is a scoped session which is good for
    all the  other tests but the purpose of this test is to make it indipendent
    to only test history_table mechanism and should therefor remain as is"""

    connection = db.engine.connect()
    transaction = connection.begin()

    session = scoped_session(sessionmaker(bind=db.engine))
    db.session = session

    def teardown():
        transaction.rollback()
        session.close_all()
        connection.close()
        remove_composite_listeners()

    request.addfinalizer(teardown)
    return session


class TestVersioning(AssertsCompiledSQL):
    __dialect__ = "default"

    @pytest.fixture
    def SomeClass(self, Base):
        class SomeClass(Versioned, Base, ComparableEntity):
            __tablename__ = "sometable"
            id = Column(Integer, primary_key=True)
            name = Column(String(50))

        return SomeClass

    @pytest.fixture()
    def BaseClass(self, Base):
        class BaseClass(Versioned, Base, ComparableEntity):
            __tablename__ = "basetable"

            id = Column(Integer, primary_key=True)
            name = Column(String(50))
            type = Column(String(20))

            __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "base"}

        return BaseClass

    @pytest.fixture()
    def SubClassSeparatePk(self, BaseClass):
        class SubClassSeparatePk(BaseClass):
            __tablename__ = "subtable1"

            id = column_property(Column(Integer, primary_key=True), BaseClass.id)
            base_id = Column(Integer, ForeignKey("basetable.id"))
            subdata1 = Column(String(50))

            __mapper_args__ = {"polymorphic_identity": "sep"}

        return SubClassSeparatePk

    @pytest.fixture()
    def SubClassSamePk(self, BaseClass):
        class SubClassSamePk(BaseClass):
            __tablename__ = "subtable2"

            id = Column(Integer, ForeignKey("basetable.id"), primary_key=True)
            subdata2 = Column(String(50))

            __mapper_args__ = {"polymorphic_identity": "same"}

        return SubClassSamePk

    @pytest.fixture()
    def SomeClass1(self, Base):
        class SomeClass1(Versioned, Base, ComparableEntity):
            __tablename__ = "sometable1"

            id = Column(Integer, primary_key=True)
            boole = Column(Boolean, default=False)

        return SomeClass1

    @pytest.fixture()
    def SomeClass2(self, Base):
        class SomeClass2(Versioned, Base, ComparableEntity):
            __tablename__ = "sometable2"

            id = Column(Integer, primary_key=True)
            name = Column(String(50))
            data = deferred(Column(String(25)))

        return SomeClass2

    @pytest.fixture()
    def SubClass(self, BaseClass):
        class SubClass(BaseClass):
            __tablename__ = "subtable"

            id = column_property(Column(Integer, primary_key=True), BaseClass.id)
            base_id = Column(Integer, ForeignKey("basetable.id"))
            subdata1 = Column(String(50))

            __mapper_args__ = {"polymorphic_identity": "sub"}

        return SubClass

    @pytest.fixture()
    def SubSubClass(self, SubClass):
        class SubSubClass(SubClass):
            __tablename__ = "subsubtable"

            id = Column(Integer, ForeignKey("subtable.id"), primary_key=True)
            subdata2 = Column(String(50))

            __mapper_args__ = {"polymorphic_identity": "subsub"}

        return SubSubClass

    @pytest.fixture()
    def Document(self, Base):
        class Document(Base, Versioned):
            __tablename__ = "document"
            id = Column(Integer, primary_key=True, autoincrement=True)
            name = Column(String, nullable=True)
            description_ = Column("description", String, nullable=True)

        return Document

    @pytest.fixture()
    def BackRefSomeRelated(self, Base):
        class BackRefSomeRelated(Base, ComparableEntity):
            __tablename__ = "backrefsomerelated"

            id = Column(Integer, primary_key=True)
            name = Column(String(50))
            related_id = Column(Integer, ForeignKey("backrefsometable.id"))
            related = relationship("BackRefSomeClass", backref="related")

        return BackRefSomeRelated

    @pytest.fixture()
    def BackRefSomeClass(self, Base):
        class BackRefSomeClass(Versioned, Base, ComparableEntity):
            __tablename__ = "backrefsometable"

            id = Column(Integer, primary_key=True)

        return BackRefSomeClass

    @pytest.fixture()
    def JoinSubClass(self, BaseClass):
        class JoinSubClass(BaseClass):
            __tablename__ = "joinsubtable"

            id = Column(Integer, ForeignKey("basetable.id"), primary_key=True)

            __mapper_args__ = {"polymorphic_identity": "sep"}

        return JoinSubClass

    @pytest.fixture()
    def InheritanceSubClass(self, BaseClass):
        class InheritanceSubClass(BaseClass):
            subname = Column(String(50), unique=True)
            __mapper_args__ = {"polymorphic_identity": "sub"}

        return InheritanceSubClass

    def test_plain(self, session1, SomeClass):
        SomeClass.metadata.create_all(session1.connection())
        versioned_session(session1)
        sess = session1
        sc = SomeClass(name="sc1")
        sess.add(sc)
        sess.commit()

        sc.name = "sc1modified"
        sess.commit()

        assert sc.resource_version == 2

        SomeClassHistory = SomeClass.__history_mapper__.class_

        eq_(
            sess.query(SomeClassHistory)
            .filter(SomeClassHistory.resource_version == 1)
            .all(),
            [SomeClassHistory(resource_version=1, name="sc1")],
        )

        sc.name = "sc1modified2"

        eq_(
            sess.query(SomeClassHistory)
            .order_by(SomeClassHistory.resource_version)
            .all(),
            [
                SomeClassHistory(resource_version=1, name="sc1"),
                SomeClassHistory(resource_version=2, name="sc1modified"),
            ],
        )

        assert sc.resource_version == 3

        sess.commit()

        sc.name = "temp"
        sc.name = "sc1modified2"

        sess.commit()

        eq_(
            sess.query(SomeClassHistory)
            .order_by(SomeClassHistory.resource_version)
            .all(),
            [
                SomeClassHistory(resource_version=1, name="sc1"),
                SomeClassHistory(resource_version=2, name="sc1modified"),
            ],
        )

        sess.delete(sc)
        sess.commit()

        eq_(
            sess.query(SomeClassHistory)
            .order_by(SomeClassHistory.resource_version)
            .all(),
            [
                SomeClassHistory(resource_version=1, name="sc1"),
                SomeClassHistory(resource_version=2, name="sc1modified"),
                SomeClassHistory(resource_version=3, name="sc1modified2"),
            ],
        )

        session1.execute(
            """
            DROP TABLE sometable CASCADE;
            DROP TABLE sometable_history CASCADE;"""
        )
        session1.commit()

    def test_w_mapper_versioning(self, session1, SomeClass):
        SomeClass.metadata.create_all(session1.connection())
        SomeClass.__mapper__.version_id_col = SomeClass.__table__.c.resource_version

        SomeClass.metadata.create_all(session1.connection())
        versioned_session(session1)
        sess = session1
        sc = SomeClass(name="sc1")
        sess.add(sc)
        sess.commit()

        s2 = Session(sess.bind)
        sc2 = s2.query(SomeClass).first()
        sc2.name = "sc1modified"

        sc.name = "sc1modified_again"
        sess.commit()

        eq_(sc.resource_version, 2)

        assert_raises(orm_exc.StaleDataError, s2.flush)

        session1.execute(
            """
            DROP TABLE sometable CASCADE;
            DROP TABLE sometable_history CASCADE;"""
        )
        session1.commit()

    def test_from_null(self, session1, SomeClass):
        SomeClass.metadata.create_all(session1.connection())
        versioned_session(session1)
        sess = session1
        sc = SomeClass()
        sess.add(sc)
        sess.commit()

        sc.name = "sc1"
        sess.commit()

        assert sc.resource_version == 2
        session1.execute(
            """
            DROP TABLE sometable CASCADE;
            DROP TABLE sometable_history CASCADE;"""
        )
        session1.commit()

    def test_insert_null(self, session1, SomeClass1):
        SomeClass1.metadata.create_all(session1.connection())
        session1.execute(
            """
            DELETE FROM sometable1 CASCADE;
            DELETE FROM sometable1_history CASCADE;"""
        )
        session1.commit()

        versioned_session(session1)
        sess = session1
        sc = SomeClass1(boole=True)
        sess.add(sc)
        sess.commit()

        sc.boole = None
        sess.commit()

        sc.boole = False
        sess.commit()

        SomeClassHistory = SomeClass1.__history_mapper__.class_

        eq_(
            sess.query(SomeClassHistory.boole).order_by(SomeClassHistory.id).all(),
            [(True,), (None,)],
        )

        eq_(sc.resource_version, 3)
        session1.execute(
            """
            DROP TABLE sometable1 CASCADE;
            DROP TABLE sometable1_history CASCADE;"""
        )
        session1.commit()

    def test_deferred(self, session1, SomeClass2):
        """test versioning of unloaded, deferred columns."""
        SomeClass2.metadata.create_all(session1.connection())
        versioned_session(session1)
        sess = session1
        sc = SomeClass2(name="sc1", data="somedata")
        sess.add(sc)
        sess.commit()
        sess.close()

        sc = sess.query(SomeClass2).first()
        assert "data" not in sc.__dict__

        sc.name = "sc1modified"
        sess.commit()

        assert sc.resource_version == 2

        SomeClassHistory = SomeClass2.__history_mapper__.class_

        eq_(
            sess.query(SomeClassHistory)
            .filter(SomeClassHistory.resource_version == 1)
            .all(),
            [SomeClassHistory(resource_version=1, name="sc1", data="somedata")],
        )

        session1.execute(
            """
            DROP TABLE sometable2 CASCADE;
            DROP TABLE sometable2_history CASCADE;"""
        )
        session1.commit()

    def test_joined_inheritance(
        self, SubClassSamePk, SubClassSeparatePk, BaseClass, session1
    ):
        SubClassSamePk.metadata.create_all(session1.connection())
        SubClassSeparatePk.metadata.create_all(session1.connection())
        BaseClass.metadata.create_all(session1.connection())

        versioned_session(session1)
        sess = session1

        sep1 = SubClassSeparatePk(name="sep1", subdata1="sep1subdata")
        base1 = BaseClass(name="base1")
        same1 = SubClassSamePk(name="same1", subdata2="same1subdata")
        sess.add_all([sep1, base1, same1])
        sess.commit()

        base1.name = "base1mod"
        same1.subdata2 = "same1subdatamod"
        sep1.name = "sep1mod"
        sess.commit()

        BaseClassHistory = BaseClass.__history_mapper__.class_
        SubClassSeparatePkHistory = SubClassSeparatePk.__history_mapper__.class_
        SubClassSamePkHistory = SubClassSamePk.__history_mapper__.class_
        eq_(
            sess.query(BaseClassHistory).order_by(BaseClassHistory.id).all(),
            [
                SubClassSeparatePkHistory(
                    id=1, name="sep1", type="sep", resource_version=1
                ),
                BaseClassHistory(id=2, name="base1", type="base", resource_version=1),
                SubClassSamePkHistory(
                    id=3, name="same1", type="same", resource_version=1
                ),
            ],
        )

        same1.subdata2 = "same1subdatamod2"

        eq_(
            sess.query(BaseClassHistory)
            .order_by(BaseClassHistory.id, BaseClassHistory.resource_version)
            .all(),
            [
                SubClassSeparatePkHistory(
                    id=1, name="sep1", type="sep", resource_version=1
                ),
                BaseClassHistory(id=2, name="base1", type="base", resource_version=1),
                SubClassSamePkHistory(
                    id=3, name="same1", type="same", resource_version=1
                ),
                SubClassSamePkHistory(
                    id=3, name="same1", type="same", resource_version=2
                ),
            ],
        )

        base1.name = "base1mod2"
        eq_(
            sess.query(BaseClassHistory)
            .order_by(BaseClassHistory.id, BaseClassHistory.resource_version)
            .all(),
            [
                SubClassSeparatePkHistory(
                    id=1, name="sep1", type="sep", resource_version=1
                ),
                BaseClassHistory(id=2, name="base1", type="base", resource_version=1),
                BaseClassHistory(
                    id=2, name="base1mod", type="base", resource_version=2
                ),
                SubClassSamePkHistory(
                    id=3, name="same1", type="same", resource_version=1
                ),
                SubClassSamePkHistory(
                    id=3, name="same1", type="same", resource_version=2
                ),
            ],
        )

        session1.execute(
            """
            DROP TABLE subtable1 CASCADE;
            DROP TABLE subtable1_history CASCADE;
            DROP TABLE subtable2 CASCADE;
            DROP TABLE subtable2_history CASCADE;
            DROP TABLE basetable CASCADE;
            DROP TABLE basetable_history CASCADE;"""
        )
        session1.commit()

    def test_joined_inheritance_multilevel(
        self, BaseClass, SubClass, SubSubClass, session1
    ):
        BaseClass.metadata.create_all(session1.connection())
        SubClass.metadata.create_all(session1.connection())
        SubSubClass.metadata.create_all(session1.connection())

        SubSubHistory = SubSubClass.__history_mapper__.class_
        versioned_session(session1)
        sess = session1
        q = sess.query(SubSubHistory)
        self.assert_compile(
            q,
            "SELECT "
            "subsubtable_history.id AS subsubtable_history_id, "
            "subtable_history.id AS subtable_history_id, "
            "basetable_history.id AS basetable_history_id, "
            "subsubtable_history.resource_changed AS "
            "subsubtable_history_resource_changed, "
            "subtable_history.resource_changed AS "
            "subtable_history_resource_changed, "
            "basetable_history.resource_changed AS "
            "basetable_history_resource_changed, "
            "basetable_history.name AS basetable_history_name, "
            "basetable_history.type AS basetable_history_type, "
            "subsubtable_history.resource_version AS "
            "subsubtable_history_resource_version, "
            "subtable_history.resource_version AS "
            "subtable_history_resource_version, "
            "basetable_history.resource_version AS "
            "basetable_history_resource_version, "
            "subtable_history.base_id AS subtable_history_base_id, "
            "subtable_history.subdata1 AS subtable_history_subdata1, "
            "subsubtable_history.subdata2 AS subsubtable_history_subdata2 "
            "FROM basetable_history "
            "JOIN subtable_history "
            "ON basetable_history.id = subtable_history.base_id "
            "AND basetable_history.resource_version = "
            "subtable_history.resource_version "
            "JOIN subsubtable_history ON subtable_history.id = "
            "subsubtable_history.id AND subtable_history.resource_version = "
            "subsubtable_history.resource_version",
        )

        ssc = SubSubClass(name="ss1", subdata1="sd1", subdata2="sd2")
        sess.add(ssc)
        sess.commit()
        eq_(sess.query(SubSubHistory).all(), [])
        ssc.subdata1 = "sd11"
        ssc.subdata2 = "sd22"
        sess.commit()
        eq_(
            sess.query(SubSubHistory).all(),
            [
                SubSubHistory(
                    name="ss1",
                    subdata1="sd1",
                    subdata2="sd2",
                    type="subsub",
                    resource_version=1,
                )
            ],
        )
        eq_(
            ssc,
            SubSubClass(
                name="ss1", subdata1="sd11", subdata2="sd22", resource_version=2
            ),
        )

        session1.execute(
            """
            DROP TABLE subsubtable CASCADE;
            DROP TABLE subsubtable_history CASCADE;
            DROP TABLE subtable CASCADE;
            DROP TABLE subtable_history CASCADE;
            DROP TABLE basetable CASCADE;
            DROP TABLE basetable_history CASCADE;"""
        )
        session1.commit()

    def test_joined_inheritance_changed(self, BaseClass, JoinSubClass, session1):
        BaseClass.metadata.create_all(session1.connection())
        JoinSubClass.metadata.create_all(session1.connection())

        BaseClassHistory = BaseClass.__history_mapper__.class_
        SubClassHistory = JoinSubClass.__history_mapper__.class_
        versioned_session(session1)
        sess = session1
        s1 = JoinSubClass(name="s1")
        sess.add(s1)
        sess.commit()

        s1.name = "s2"
        sess.commit()

        actual_changed_base = sess.scalar(
            select([BaseClass.__history_mapper__.local_table.c.resource_changed])
        )
        actual_changed_sub = sess.scalar(
            select([JoinSubClass.__history_mapper__.local_table.c.resource_changed])
        )
        h1 = sess.query(BaseClassHistory).first()
        eq_(h1.resource_changed, actual_changed_base)
        eq_(h1.resource_changed, actual_changed_sub)

        h1 = sess.query(SubClassHistory).first()
        eq_(h1.resource_changed, actual_changed_base)
        eq_(h1.resource_changed, actual_changed_sub)

        session1.execute(
            """
            DROP TABLE joinsubtable CASCADE;
            DROP TABLE joinsubtable_history CASCADE;
            DROP TABLE basetable CASCADE;
            DROP TABLE basetable_history CASCADE;"""
        )
        session1.commit()

    def test_single_inheritance(self, InheritanceSubClass, BaseClass, session1):
        BaseClass.metadata.create_all(session1.connection())
        InheritanceSubClass.metadata.create_all(session1.connection())

        versioned_session(session1)
        sess = session1

        b1 = BaseClass(name="b1")
        sc = InheritanceSubClass(name="s1", subname="sc1")

        sess.add_all([b1, sc])

        sess.commit()

        b1.name = "b1modified"

        BaseClassHistory = BaseClass.__history_mapper__.class_
        InheritanceSubClassHistory = InheritanceSubClass.__history_mapper__.class_

        eq_(
            sess.query(BaseClassHistory)
            .order_by(BaseClassHistory.id, BaseClassHistory.resource_version)
            .all(),
            [BaseClassHistory(id=1, name="b1", type="base", resource_version=1)],
        )

        sc.name = "s1modified"
        b1.name = "b1modified2"

        eq_(
            sess.query(BaseClassHistory)
            .order_by(BaseClassHistory.id, BaseClassHistory.resource_version)
            .all(),
            [
                BaseClassHistory(id=1, name="b1", type="base", resource_version=1),
                BaseClassHistory(
                    id=1, name="b1modified", type="base", resource_version=2
                ),
                InheritanceSubClassHistory(
                    id=2, name="s1", type="sub", resource_version=1
                ),
            ],
        )

        # test the unique constraint on the subclass column
        sc.name = "modifyagain"
        sess.flush()

        session1.execute(
            """
            DROP TABLE basetable CASCADE;
            DROP TABLE basetable_history CASCADE;"""
        )
        session1.commit()

    def test_unique(self, SomeClass2, session1):
        SomeClass2.metadata.create_all(session1.connection())

        versioned_session(session1)
        sess = session1
        sc = SomeClass2(name="sc1", data="sc1")
        sess.add(sc)
        sess.commit()

        sc.data = "sc1modified"
        sess.commit()

        assert sc.resource_version == 2

        sc.data = "sc1modified2"
        sess.commit()

        assert sc.resource_version == 3

        session1.execute(
            """
            DROP TABLE sometable2 CASCADE;
            DROP TABLE sometable2_history CASCADE;"""
        )
        session1.commit()

    # # @pytest.fixture()
    # # def RelSomeRelated(self, Base):
    # #     class RelSomeRelated(Base, ComparableEntity):
    # #         __tablename__ = 'relsomerelated'
    # #
    # #         id = Column(Integer, primary_key=True)
    # #
    # #     return RelSomeRelated
    # #
    # # @pytest.fixture()
    # # def RelSomeClass(self, Base):
    # #     class RelSomeClass(Versioned, Base, ComparableEntity):
    # #         __tablename__ = 'relsometable'
    # #
    # #         id = Column(Integer, primary_key=True)
    # #         name = Column(String(50))
    # #         related_id = Column(Integer, ForeignKey('relsomerelated.id'))
    # #         related = relationship("RelSomeRelated", backref='classes')
    # #
    # #     return RelSomeClass
    # #
    # # def test_relationship(self, RelSomeClass, RelSomeRelated,
    # #                       session1):
    # #     RelSomeRelated.metadata.create_all(session1.connection())
    # #     RelSomeClass.metadata.create_all(session1.connection())
    # #     SomeClassHistory = RelSomeClass.__history_mapper__.class_
    # #
    # #     versioned_session(session1)
    # #     sess = session1
    # #
    # #     sc = RelSomeClass(name='sc1')
    # #     sess.add(sc)
    # #     sess.commit()
    # #
    # #     assert sc.resource_version == 1
    # #
    # #     sr1 = RelSomeClass()
    # #     sc.related = sr1
    # #     sess.commit()
    # #
    # #     assert sc.resource_version == 2
    #
    # # eq_(
    # #     sess.query(SomeClassHistory).filter(
    # #         SomeClassHistory.resource_version == 1).all(),
    # #     [SomeClassHistory(version=1, name='sc1', related_id=None)]
    # # )
    # #
    # # sc.related = None
    # #
    # # eq_(
    # #     sess.query(SomeClassHistory).order_by(
    # #         SomeClassHistory.resource_version).all(),
    # #     [
    # #         SomeClassHistory(version=1, name='sc1', related_id=None),
    # #         SomeClassHistory(version=2, name='sc1', related_id=sr1.id)
    # #     ]
    # # )
    # #
    # # assert sc.resource_version == 3

    def test_backref_relationship(self, BackRefSomeRelated, BackRefSomeClass, session1):
        BackRefSomeRelated.metadata.create_all(session1.connection())
        BackRefSomeClass.metadata.create_all(session1.connection())

        versioned_session(session1)
        sess = session1
        sc = BackRefSomeClass()
        sess.add(sc)
        sess.commit()

        assert sc.resource_version == 1

        sr = BackRefSomeRelated(name="sr", related=sc)
        sess.add(sr)
        sess.commit()

        assert sc.resource_version == 1

        sr.name = "sr2"
        sess.commit()

        assert sc.resource_version == 1

        sess.delete(sr)
        sess.commit()

        assert sc.resource_version == 1

        session1.execute(
            """
            DROP TABLE backrefsometable CASCADE;
            DROP TABLE backrefsometable_history CASCADE;
            DROP TABLE backrefsomerelated CASCADE;"""
        )
        session1.commit()

    def test_create_double_flush(self, Document, session1):
        Document.metadata.create_all(session1.connection())

        versioned_session(session1)

        sc = Document()
        session1.add(sc)
        session1.flush()
        sc.name = "Foo"
        session1.flush()

        assert sc.resource_version == 2

        session1.execute(
            """
            DROP TABLE document CASCADE;
            DROP TABLE document_history CASCADE;"""
        )
        session1.commit()

    def test_mutate_plain_column(self, Document, session1):
        Document.metadata.create_all(session1.connection())

        versioned_session(session1)

        document = Document()
        session1.add(document)
        document.name = "Foo"
        session1.commit()
        document.name = "Bar"
        session1.commit()

        DocumentHistory = Document.__history_mapper__.class_
        v2 = session1.query(Document).one()
        v1 = session1.query(DocumentHistory).one()
        assert v1.id == v2.id
        assert v2.name == "Bar"
        assert v1.name == "Foo"

        session1.execute(
            """
            DROP TABLE document CASCADE;
            DROP TABLE document_history CASCADE;"""
        )
        session1.commit()

    def test_mutate_named_column(self, Document, session1):
        Document.metadata.create_all(session1.connection())

        versioned_session(session1)

        document = Document()
        session1.add(document)
        document.description_ = "Foo"
        session1.commit()
        document.description_ = "Bar"
        session1.commit()

        DocumentHistory = Document.__history_mapper__.class_
        v2 = session1.query(Document).one()
        v1 = session1.query(DocumentHistory).one()
        assert v1.id == v2.id
        assert v2.description_ == "Bar"
        assert v1.description_ == "Foo"

        session1.execute(
            """
            DROP TABLE document CASCADE;
            DROP TABLE document_history CASCADE;"""
        )
        session1.commit()
