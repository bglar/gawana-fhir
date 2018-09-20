""" All resources in this server should be registered in this file """

from .conformance import *
from .identification import *
from .infrastructure import *

all_resources = [
    Organization,
    Patient,
    Practitioner,
    HealthcareService,
    Location,
    StructureDefinition,
    ValueSet,
    OperationOutcome
]
constraints = []

from datetime import datetime, timezone  # noqa
from sqlalchemy import event  # noqa
for resource in all_resources:
    """An event hook adds missing text field on all resources.

    Resources should have a human readable text field that can be used
    to render a resource instance. Each resource that implements
    `_resource_summary` func will have a text field created from that method.
    """
    @event.listens_for(resource, "before_insert")
    @event.listens_for(resource, "before_update")
    def gen_default(mapper, connection, instance):
        now = datetime.now(timezone.utc)
        str_now = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S%z')
        rep = instance._resource_summary().get('repr')
        div = '<div xmlns="http://www.w3.org/1999/xhtml">{}</div>'.format(rep)
        narrative = {
            'div': div,
            'status': 'generated'
        }
        instance.text = narrative

        if not instance.meta:
            instance.meta = {}

        if isinstance(instance.meta, dict):
            if not instance.meta.get('lastUpdated'):
                instance.meta['lastUpdated'] = str_now
        else:
            if not instance.meta.lastUpdated:
                instance.meta._replace(lastUpdated=str_now)
