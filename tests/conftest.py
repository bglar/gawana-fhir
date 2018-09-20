import os
import warnings

import pytest
from sqlalchemy.exc import StatementError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import remove_composite_listeners

from fhir_server.app import db as _db

from fhir_server.app import create_app
from fhir_server.elements.base.pg_types import register_pg_types


def create_my_app(config=None):
    app = create_app(config)
    return app


_app = create_app()


@pytest.fixture
def Base():
    return declarative_base()


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    _app.config.from_object(os.environ['TEST_SETTINGS'])

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""

    def teardown():
        # Teardown only fails when dropping composite types. Composite types
        # are not dynamic on test runs and therefor they should be maintained
        # to speed up testing
        try:
            _db.drop_all()
        except StatementError as excinfo:
            warnings.warn(excinfo.__repr__(),
                          category=UserWarning, stacklevel=1)

    _db.app = app
    register_pg_types(_db.session)
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    session = db.create_scoped_session(options={'bind': connection})
    # session = db.create_scoped_session()

    db.session = session

    def teardown():
        transaction.rollback()
        session.close_all()
        connection.close()
        remove_composite_listeners()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='function')
def client(app, session, request):
    def teardown():
        session.close_all()
        remove_composite_listeners()

    request.addfinalizer(teardown)
    return app.test_client()
