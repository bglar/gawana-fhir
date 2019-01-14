import fileinput
import os
import sys

from flask import current_app, url_for
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy_utils import register_composites

from fhir_server.app import create_app, db
from fhir_server.oauth_server.urls import oauth


def create_my_app(config=None):
    app = create_app(config)
    return app


migrations_path = "/migrations/versions/"
app = create_my_app()
app.config.from_object(os.environ["APP_SETTINGS"])

app = create_app()
conn = db.session.connection()
register_composites(conn)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
manager.add_option(
    "-c", "--config", dest="config", required=False, help="config [local, dev, prod]"
)


@manager.command
def run():
    """Run in local machine."""
    port = int(os.environ.get("PORT", 5000))
    current_app.run(host="0.0.0.0", port=port, debug=True)


@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all(bind=None)
    db.create_all(bind=None)


@manager.command
def clean_migrations():
    """cleans up migrations removing unnecessary arguments from autogenerate.

    Migrations for complex types generate a table=None argument for all the
    resources. We should inspect the files and remove this argument"""

    path = os.path.realpath(".") + migrations_path
    for subdir, dirs, files in os.walk(path):
        for file in [pyfiles for pyfiles in files if pyfiles.endswith(".py")]:
            for line in fileinput.input(os.path.join(path, file), inplace=1):
                sys.stdout.write(line.replace(", table=None", ""))


@app.route("/")
@oauth.require_oauth()
def api_index():
    """Glar FHIR Server
    -------------------------

    **What is FHIR (Fast Healthcare Interoperability Resources)**

    `FHIR` is a standard for exchanging healthcare information electronically.
    The FHIR (pronounced "fire") standard uses basic building blocks called
    `resources` to model healthcare data in a way that is easier for
    healthcare providers to use and share clinical data as needed without
    compromising security or violating HIPAA (Health Insurance Portability and
    Accountability Act).

    The specification for FHIR is created and maintained by
    HL7 (Health Level 7) International, the organization responsible for the
    HL7 v2 and HL7 v3 standards that are widely used in healthcare messaging
    today.

    **Getting started with the server**

    1. **READ**

        The read interaction accesses the current contents of a resource.

        - GET / LIST Resources:
        `[base]/[resource_name]/`

                http://localhost:5000/api/v1/Organization

        - GET / RETRIEVE Resource by logical Identifier:
        `[base]/[resource_name]/[id]/`

                http://localhost:5000/api/v1/Organization/123-abc-org1/

        - GET / RETRIEVE Resource summary:
        `[base]/[resource_name]/[id]/?_summary/`

                http://localhost:5000/api/v1/Organization/123-abc-org1/?_summary/

    2. **VREAD**

        The vread interaction preforms a version specific read of the resource.

        - GET / LIST Resource Histories:
        `[base]/[resource_name]/_history/`

                http://localhost:5000/api/v1/Organization/_history

        - GET / RETRIEVE Resource versions by Logical Identifier and Version:
         `[base]/[resource_name]/[id]/_history/`

                http://localhost:5000/api/v1/Organization/123-abc-org1/_history/

    3. **POST**

        Creates a new resource in a server-assigned location.
        If the client wishes to have control over the id of a newly submitted
        resource, it should use the update interaction instead.

        - POST / CREATE Resources:
            `[base]/[resource_name]/`

                    http://localhost:5000/api/v1/Organization/

        - POST / CONDITIONAL CREATE: Allows a client to create a new resource
        only if some equivalent resource does not already exist on the server.
        The client defines what equivalence means in this case by supplying a
        FHIR search query in an If-None-Exist header as shown

            `If-None-Exist: [search parameters]`


    4. **PUT**

        Creates a new current version for an existing resource or creates an
        initial version if no resource already exists for the given id.

        - POST / UPDATE Resources:
            `[base]/[resource_name]/[id]`

                    http://localhost:5000/api/v1/Organization/123-abc

        - POST / CONDITIONAL UPDATE: Allows a client to update an existing
        resource based on some identification criteria, rather than by id

            `[base]/[resource_name]?[search_parameters]`



    5. **DELETE**

         Removes an existing resource.

        - DELETE / REMOVE Resources:
            `[base]/[resource_name]/[id]`

                    http://localhost:5000/api/v1/Organization/123-abc

        - POST / CONDITIONAL UPDATE: Allows a client to update an existing
        resource based on some identification criteria, rather than by id

            `[base]/[resource_name]?[search_parameters]`

    More interactions on this server are defined
    [here](http://hl7.org/fhir/2016Sep/http.html)

    """

    links = []
    domain = app.config["DOMAIN_NAME"]

    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append("http://" + domain + url)

    # return "Hello, %s!" % g.user
    return links


if __name__ == "__main__":
    manager.run()
    register_composites(conn)
