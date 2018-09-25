Gawana FHIR Server
===============

What is FHIR (Fast Healthcare Interoperability Resources)
---------------------------------------------------------

FHIR_ is a standard for exchanging healthcare information electronically.
The FHIR (pronounced "fire") standard uses basic building blocks called
**resources** to model healthcare data in a way that is easier for healthcare
providers to use and share clinical data as needed without compromising
security or violating HIPAA (Health Insurance Portability and Accountability Act).

The specification for FHIR is created and maintained by
HL7_ (Health Level 7) International, the organization responsible for the
HL7 v2 and HL7 v3 standards that are widely used in healthcare messaging today.

.. _FHIR: https://www.hl7.org/fhir/
.. _HL7: http://www.hl7.org/

Getting Started
---------------

These instructions will get you a copy of the server up and running on your
local machine for development and testing purposes. See Deployment for notes on
how to deploy the project on a live system.

Prerequisites
~~~~~~~~~~~~~

You will need the following installed before you can run the server::

    pip
    Python3.7.0
    Python3.7.0-dev
    PostgreSQL
    pguri
    virtualenvwrapper

Installing pguri (uri type for PostgreSQL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pguri_ is an extension for PostgreSQL that provides a uri data type and allows
the following operations:

    - URI syntax checking
    - functions for extracting URI components
    - human-friendly sorting

.. _pguri: https://github.com/petere/pguri/

Install liburiparser-dev on Ubuntu::

    $ sudo apt-get update
    $ sudo apt-get install liburiparser-dev


For MaxOS you will need to install the following::

    $ brew install pkg-config
    $ brew install uriparser

Install pguri::

    $ cd lib/pguri
    $ make
    $ make install

If the installation throws an error of this nature::

    $ Makefile:20: /usr/lib/postgresql/9.5/lib/pgxs/src/makefiles/pgxs.mk: No such file or directory
    $ make: *** No rule to make target `/usr/lib/postgresql/9.5/lib/pgxs/src/makefiles/pgxs.mk'.  Stop.

be sure to install postgresql-server-dev-version. You can use the following commands to install
a version that corresponds to your installed postgresql version::

    $ which psql
    $ sudo apt-get install postgresql-server-dev-9.5
    $ # 9.5 is my postgresql version, replace it with your installed version

You may need to repeat the command in the Install pguri section.

Create a uri extension in the database::

    $ CREATE EXTENSION uri

Setting up project environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone and go to the project directory::

    $ git clone git@github.com:bglar/gawana_fhir_server.git
    $ cd path/to/project/directory/gawana_fhir_server

Create a py3.5.1 virtual environment::

    $ mkvirtualenv --python=/usr/bin/python3.5.1 env_name # env_name is the name of your virtual environment

Configure environment variables to use whenever the virtual environment is activated::

    $ vim ~/{virtualenv_folder_path}/{env_name}/bin/postactivate
    # Add the following lines to the open file and then save.
    #
    # cd /home/glar/Gawana/gawana_fhir_server/
    # export DATABASE_URL='postgres://ubuntu:@127.0.0.1:5432/gawana_fhir'
    # export TEST_DATABASE_URL='postgres://ubuntu:@127.0.0.1:5432/test_gawana_fhir'
    # export APP_SETTINGS='fhir_server.configs.base.DevelopmentConfig'
    # export TEST_SETTINGS='fhir_server.configs.base.TestingConfig'

Install the requirements::

    $ pip install -r requirements/dev.txt

Local Migration
~~~~~~~~~~~~~~~

We are using Alembic and Flask-Migrate to migrate our database to the
latest version. Alembic is migration library for SQLAlchemy and could be used
without Flask-Migrate if you want. However Flask-Migrate does help with some of
the setup and makes things easier.

To make migrations and update the db run the following commands::

    $ python manage.py db migrate -m "relevant migration message"
    $ python manage.py clean_up_migrations
    $ python manage.py db upgrade

The generated migration creates a `table=None` attribute for every field in the
`PgComposite` types. The command `clean_up_migrations` is a helper in cleaning up
these files and therefore it should not be ignored.

Running the tests
-----------------

Install the test requirements and run test command::

    $ pip install -r requirements-test.txt
    $ tox

Deployment
----------

To deploy this project create a python2 virtual environment::

    $ mkvirtualenv --python=/usr/bin/python2.7 env_name # env_name is the name of your virtual environment

Install the deployment dependencies to your virtual environment::

    $ pip install -r requirements-deploy.txt

Authors
-------

`Brian Ogollah`_

.. _`Brian Ogollah`: https://github.com/bglar
