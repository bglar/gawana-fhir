"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision}
Create Date: ${create_date}

"""

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column
import sqlalchemy_utils
from sqlalchemy_utils import CompositeArray, JSONType

import fhir_server
from fhir_server.elements.primitives import *
from fhir_server.elements.opentype import OpenType
from fhir_server.elements.base.complex_mixin import PgComposite
${imports if imports else ""}

from fhir_server.resources import all_resources, constraints

def upgrade():
    ${upgrades if upgrades else "pass"}

    conn = op.get_bind()
    for resource in all_resources:
        conn.execute(sa.sql.text(
            '''
            DROP INDEX IF EXISTS {0}_meta_version_id;

            CREATE UNIQUE INDEX {0}_meta_version_id ON {0} (
                ((meta).version_id));

            DROP TRIGGER IF EXISTS meta_version_id_concurrency ON {0};

            CREATE TRIGGER meta_version_id_concurrency BEFORE INSERT OR UPDATE ON {0}
            FOR EACH ROW EXECUTE PROCEDURE meta_version_id_concurrency();
            '''.format(resource.__tablename__)
        ))

    profiled_resources = {con.get('resource'): con.get('fields') for con in constraints}
    for resource, const in profiled_resources.items():
        for c in const:
            field = c.get('name')
            mini = str(c.get('cardinality').get('mini'))
            maxi = str(c.get('cardinality').get('maxi'))
            conn.execute(sa.sql.text(
                '''
                DROP TRIGGER IF EXISTS validate_meta_fields_{1} ON {0};

                CREATE TRIGGER validate_meta_fields_{1} BEFORE INSERT OR UPDATE ON {0}
                FOR EACH ROW EXECUTE PROCEDURE validate_meta_fields({1}, '{2}', '{3}');
                '''.format(resource.lower(), field, mini, maxi)
            ))


def downgrade():
    ${downgrades if downgrades else "pass"}
