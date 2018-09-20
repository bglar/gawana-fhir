"""structdef resource

Revision ID: f8787deba0e9
Revises: 9800e50d3c16
Create Date: 2016-06-29 13:44:23.937493

"""

# revision identifiers, used by Alembic.
revision = 'f8787deba0e9'
down_revision = '9800e50d3c16'

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column
import sqlalchemy_utils
from sqlalchemy_utils import CompositeArray

import fhir_server
from fhir_server.elements.primitives import *
from fhir_server.elements.opentype import OpenType
from fhir_server.elements.base.complex_mixin import PgComposite


from fhir_server.resources import all_resources, constraints

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('structuredefinition',
    sa.Column('id', fhir_server.elements.primitives.IdField(), nullable=False),
    sa.Column('implicitRules', fhir_server.elements.primitives.URIField(), nullable=True),
    sa.Column('language', fhir_server.elements.primitives.CodeField(), nullable=True),
    sa.Column('url', fhir_server.elements.primitives.URIField(), nullable=False),
    sa.Column('version', fhir_server.elements.primitives.StringField(), nullable=True),
    sa.Column('name', fhir_server.elements.primitives.StringField(), nullable=False),
    sa.Column('display', fhir_server.elements.primitives.StringField(), nullable=True),
    sa.Column('status', fhir_server.elements.primitives.CodeField(), nullable=False),
    sa.Column('experimental', fhir_server.elements.primitives.BooleanField(), nullable=True),
    sa.Column('publisher', fhir_server.elements.primitives.StringField(), nullable=True),
    sa.Column('date', fhir_server.elements.primitives.DateTimeField(timezone=True), nullable=True),
    sa.Column('description', fhir_server.elements.primitives.StringField(), nullable=True),
    sa.Column('requirements', fhir_server.elements.primitives.StringField(), nullable=True),
    sa.Column('copyright', fhir_server.elements.primitives.StringField(), nullable=True),
    sa.Column('fhirVersion', fhir_server.elements.primitives.IdField(), nullable=True),
    sa.Column('kind', fhir_server.elements.primitives.CodeField(), nullable=False),
    sa.Column('constrainedType', fhir_server.elements.primitives.CodeField(), nullable=True),
    sa.Column('abstract', fhir_server.elements.primitives.BooleanField(), nullable=False),
    sa.Column('context', sqlalchemy_utils.types.pg_composite.CompositeArray(StringField()), nullable=True),
    sa.Column('contextType', fhir_server.elements.primitives.CodeField(), nullable=True),
    sa.Column('base', fhir_server.elements.primitives.URIField(), nullable=True),
    sa.Column('identifier', sqlalchemy_utils.types.pg_composite.CompositeArray(PgComposite('fhir_identifier', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('system', URIField()), Column('use', CodeField()), Column('value', StringField()), Column('assigner', PgComposite('fhir_reference', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('display', StringField()), Column('reference', StringField())])), Column('period', PgComposite('fhir_period', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('end_time', DateTimeField(timezone=True)), Column('start_time', DateTimeField(timezone=True))])), Column('type', PgComposite('fhir_codeableconcept', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('text', StringField()), Column('coding', CompositeArray(PgComposite('fhir_coding', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('code', CodeField()), Column('display', StringField()), Column('system', URIField()), Column('user_selected', BooleanField()), Column('version', StringField())])))]))])), nullable=True),
    sa.Column('useContext', sqlalchemy_utils.types.pg_composite.CompositeArray(PgComposite('fhir_codeableconcept', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('text', StringField()), Column('coding', CompositeArray(PgComposite('fhir_coding', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('code', CodeField()), Column('display', StringField()), Column('system', URIField()), Column('user_selected', BooleanField()), Column('version', StringField())])))])), nullable=True),
    sa.Column('code', sqlalchemy_utils.types.pg_composite.CompositeArray(PgComposite('fhir_coding', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('code', CodeField()), Column('display', StringField()), Column('system', URIField()), Column('user_selected', BooleanField()), Column('version', StringField())])), nullable=True),
    sa.Column('contact', sqlalchemy_utils.types.pg_composite.CompositeArray(PgComposite('fhir_structuredefinitioncontact', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('name', StringField()), Column('telecom', CompositeArray(PgComposite('fhir_contactpoint', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('rank', PositiveIntField()), Column('system', CodeField()), Column('use', CodeField()), Column('value', StringField()), Column('period', PgComposite('fhir_period', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('end_time', DateTimeField(timezone=True)), Column('start_time', DateTimeField(timezone=True))]))])))])), nullable=True),
    sa.Column('mapping', sqlalchemy_utils.types.pg_composite.CompositeArray(PgComposite('fhir_structuredefinitionmapping', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('identity', IdField(), nullable=False), Column('uri', URIField()), Column('name', StringField()), Column('comments', StringField())])), nullable=True),
    sa.Column('differential', fhir_server.elements.base.complex_mixin.PgComposite('fhir_structuredefinitiondifferential', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('element', CompositeArray(PgComposite('fhir_elementdefinition', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('path', StringField(), nullable=False), Column('representation', CompositeArray(CodeField())), Column('name', StringField()), Column('label', StringField()), Column('short', StringField()), Column('definition', MarkdownField()), Column('comments', MarkdownField()), Column('requirements', MarkdownField()), Column('alias', CompositeArray(StringField())), Column('min', IntegerField()), Column('max', StringField()), Column('nameReference', StringField()), Column('meaningWhenMissing', MarkdownField()), Column('maxLength', IntegerField()), Column('condition', CompositeArray(IdField())), Column('mustSupport', BooleanField()), Column('isModifier', BooleanField()), Column('isSummary', BooleanField()), Column('defaultValue', OpenType()), Column('fixed', OpenType()), Column('pattern', OpenType()), Column('example', OpenType()), Column('minValue', OpenType()), Column('maxValue', OpenType()), Column('code', CompositeArray(PgComposite('fhir_coding', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('code', CodeField()), Column('display', StringField()), Column('system', URIField()), Column('user_selected', BooleanField()), Column('version', StringField())]))), Column('slicing', PgComposite('fhir_elementdefinitionslicing', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('description', StringField()), Column('discriminator', CompositeArray(StringField())), Column('ordered', BooleanField()), Column('rules', CodeField(), nullable=False)])), Column('base', PgComposite('fhir_elementdefinitionbase', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('max', StringField(), nullable=False), Column('min', IntegerField(), nullable=False), Column('path', StringField(), nullable=False)])), Column('elementDefinitionType', CompositeArray(PgComposite('fhir_elementdefinitiontype', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('aggregation', CompositeArray(CodeField())), Column('code', StringField(), nullable=False), Column('profile', CompositeArray(URIField()))]))), Column('constraint', CompositeArray(PgComposite('fhir_elementdefinitionconstraint', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('human', StringField(), nullable=False), Column('key', IdField(), nullable=False), Column('requirements', StringField()), Column('severity', CodeField(), nullable=False), Column('xpath', StringField(), nullable=False)]))), Column('binding', PgComposite('fhir_elementdefinitionbinding', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('description', StringField()), Column('strength', CodeField(), nullable=False), Column('valueSetReference', PgComposite('fhir_reference', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('display', StringField()), Column('reference', StringField())])), Column('valueSetUri', URIField())])), Column('mapping', CompositeArray(PgComposite('fhir_elementdefinitionmapping', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('identity', IdField(), nullable=False), Column('language', CodeField()), Column('map', StringField(), nullable=False)])))])), nullable=False)]), nullable=True),
    sa.Column('snapshot', fhir_server.elements.base.complex_mixin.PgComposite('fhir_structuredefinitionsnapshot', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('element', PgComposite('fhir_elementdefinition', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('path', StringField(), nullable=False), Column('representation', CompositeArray(CodeField())), Column('name', StringField()), Column('label', StringField()), Column('short', StringField()), Column('definition', MarkdownField()), Column('comments', MarkdownField()), Column('requirements', MarkdownField()), Column('alias', CompositeArray(StringField())), Column('min', IntegerField()), Column('max', StringField()), Column('nameReference', StringField()), Column('meaningWhenMissing', MarkdownField()), Column('maxLength', IntegerField()), Column('condition', CompositeArray(IdField())), Column('mustSupport', BooleanField()), Column('isModifier', BooleanField()), Column('isSummary', BooleanField()), Column('defaultValue', OpenType()), Column('fixed', OpenType()), Column('pattern', OpenType()), Column('example', OpenType()), Column('minValue', OpenType()), Column('maxValue', OpenType()), Column('code', CompositeArray(PgComposite('fhir_coding', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('code', CodeField()), Column('display', StringField()), Column('system', URIField()), Column('user_selected', BooleanField()), Column('version', StringField())]))), Column('slicing', PgComposite('fhir_elementdefinitionslicing', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('description', StringField()), Column('discriminator', CompositeArray(StringField())), Column('ordered', BooleanField()), Column('rules', CodeField(), nullable=False)])), Column('base', PgComposite('fhir_elementdefinitionbase', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('max', StringField(), nullable=False), Column('min', IntegerField(), nullable=False), Column('path', StringField(), nullable=False)])), Column('elementDefinitionType', CompositeArray(PgComposite('fhir_elementdefinitiontype', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('aggregation', CompositeArray(CodeField())), Column('code', StringField(), nullable=False), Column('profile', CompositeArray(URIField()))]))), Column('constraint', CompositeArray(PgComposite('fhir_elementdefinitionconstraint', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('human', StringField(), nullable=False), Column('key', IdField(), nullable=False), Column('requirements', StringField()), Column('severity', CodeField(), nullable=False), Column('xpath', StringField(), nullable=False)]))), Column('binding', PgComposite('fhir_elementdefinitionbinding', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('description', StringField()), Column('strength', CodeField(), nullable=False), Column('valueSetReference', PgComposite('fhir_reference', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('display', StringField()), Column('reference', StringField())])), Column('valueSetUri', URIField())])), Column('mapping', CompositeArray(PgComposite('fhir_elementdefinitionmapping', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('identity', IdField(), nullable=False), Column('language', CodeField()), Column('map', StringField(), nullable=False)])))]), nullable=False)]), nullable=True),
    sa.Column('meta', fhir_server.elements.base.complex_mixin.PgComposite('fhir_meta', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('version_id', IdField()), Column('last_updated', InstantField(timezone=True)), Column('profile', CompositeArray(URIField())), Column('security', CompositeArray(PgComposite('fhir_coding', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('code', CodeField()), Column('display', StringField()), Column('system', URIField()), Column('user_selected', BooleanField()), Column('version', StringField())]))), Column('tag', CompositeArray(PgComposite('fhir_coding', [Column('extension', PgComposite('fhir_extension', [Column('url', StringField(), nullable=False), Column('value', OpenType())])), Column('id', StringField()), Column('code', CodeField()), Column('display', StringField()), Column('system', URIField()), Column('user_selected', BooleanField()), Column('version', StringField())])))]), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###

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
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('structuredefinition')
    ### end Alembic commands ###
