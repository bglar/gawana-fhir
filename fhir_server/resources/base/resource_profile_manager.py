import xmltodict
import re
from sqlalchemy_utils import CompositeArray

from fhir_server.resources import all_resources, constraints as constr


class ResourceProfile(object):
    """Mechanism for interpreting profiled resources (resource constraints).

    Expect a dict in the format shown in Variables section below.
    The is used to constrain the resources based on a profile. For element
    profiles use `fhir_server.elements.base.complex_elements`

    Variables:
        {
            'resource': 'Address',
            'fields':  [
                {
                    'name': 'city',
                    'cardinality': {
                        'mini': '0',
                        'maxi': '1'
                    }
                },
                {
                    'name': 'contact',
                    'cardinality': {
                        'mini': '1',
                        'maxi': '*'
                    }
                }
            ]
        }
    """

    def __init__(self, constraints):
        self.resource_name = constraints.get('resource')
        self.fields = constraints.get('fields')
        self.resource_instance = {}
        self.profiled_columns = []
        constr.append(constraints)

        if self.resource_name is None:
            raise Exception(
                "Missing Key: resource",
                "It's value should be name of a fhir resource")
        else:
            self.resource_name = self.resource_name.lower()

        if self.fields is None:
            raise Exception(
                'Missing Key: fields',
                'Should have a field name and cardinality')

        self.apply_constraints()

    def apply_constraints(self):
        for resource in all_resources:
            self.resource_instance[resource.__tablename__.lower()] = resource

        if self.resource_name in self.resource_instance:
            res = self.resource_instance.get(self.resource_name)

            for field in self.fields:
                name = field.get('name')
                cardinality = field.get('cardinality')

                # get the column from schema definition
                col = res.__table__.columns.get(name)
                if col is not None:
                    default_type = col.type

                    if cardinality['mini'] == '1' and col.nullable:
                        col.nullable = False

                    if cardinality['maxi'] == '*' and not (
                            isinstance(col.type, CompositeArray)):

                        col.type = CompositeArray(default_type)

                    self.profiled_columns.append(col)

            # replace the schema definition with our profile definition
            for column in self.profiled_columns:
                res.__table__.columns.replace(column)

            return res

        else:
            raise Exception(
                'Missing Resource',
                'The resource is not available in this server or it has '
                'not been registered')


class XMLProfileManager(object):
    """Mechanism for interpreting profiled resources from xml.

    This manager will read profiles from xml file and apply the constraints to
    the models. The xml file should be a standard xml file such as one generated
    by [**Fhir DSTU-2 Forge**](http://fhir.furore.com/Forge).
    The differential component of the profile is used to get any changes that
    have been made on the default profile that ships with fhir.

    Variables:
        String: 'file/path/to/your/{profile}.xml/'
    """

    def __init__(self, file_path):
        with open(file_path) as fd:
            self.doc = xmltodict.parse(fd.read())
            self.resource_name = ''
            self.resource_fields = []
            self.constraints = {
                'resource': '',
                'fields': []
            }

            profiled_fields = self.construct_constraints()
            ResourceProfile(profiled_fields)

    def construct_constraints(self):

        for key, element in enumerate(
                (self.doc['StructureDefinition']['differential']['element'])):

            if key == 0:
                # The 1st element is always the Resource
                self.resource_name = element['path']['@value']
                self.constraints['resource'] = self.resource_name

            else:
                field_path = element['path']['@value']
                field = re.sub(self.resource_name + '.', '', field_path, 1)

                new_min = element['min']['@value']
                new_max = element['max']['@value']

                data = {
                    'name': field,
                    'cardinality': {
                        'mini': new_min,
                        'maxi': new_max
                    }
                }
                self.constraints['fields'].append(data)
        return self.constraints
