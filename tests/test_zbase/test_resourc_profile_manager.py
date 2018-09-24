import pytest

from fhir_server.configs import BASE_DIR
from fhir_server.resources.base.resource_profile_manager import (
    ResourceProfile,
    XMLProfileManager
)


def test_init_with_valid_constraints():
    constraints = {
        'resource': 'Organization',
        'fields': [
            {'name': 'active', 'cardinality': {'mini': '1', 'maxi': '1'}},
            {'name': 'name', 'cardinality': {'mini': '1', 'maxi': '1'}},
            {'name': 'identifier', 'cardinality': {'mini': '1', 'maxi': '*'}}
        ]
    }

    org_profile = ResourceProfile(constraints)
    assert org_profile.resource_name == 'organization'


def test_init_with_constraints_missing_resource():
    constraints = {
        'fields': [
            {'name': 'active', 'cardinality': {'mini': 0, 'maxi': '1'}},
            {'name': 'name', 'cardinality': {'mini': 0, 'maxi': '1'}},
            {'name': 'identifier', 'cardinality': {'mini': 0, 'maxi': '*'}}
        ]
    }

    with pytest.raises(Exception) as execinfo:
        ResourceProfile(constraints)
    assert "Missing Key: resource" in str(execinfo.value)


def test_init_with_constraints_missing_fields():
    constraints = {
        'resource': 'Organization'
    }

    with pytest.raises(Exception) as execinfo:
        ResourceProfile(constraints)
    assert "Missing Key: fields" in str(execinfo.value)


def test_apply_constraints():
    constraints = {
        'resource': 'Organization',
        'fields': [
            {'name': 'active', 'cardinality': {'mini': 0, 'maxi': '1'}},
            {'name': 'name', 'cardinality': {'mini': '1', 'maxi': '1'}},
            {'name': 'identifier', 'cardinality': {'mini': '1', 'maxi': '*'}}
        ]
    }

    org_profile = ResourceProfile(constraints)
    DemoOrgResource = org_profile.apply_constraints()
    assert DemoOrgResource.__tablename__ == 'Organization'


def test_apply_constraints_with_resource_name_that_does_not_exist():
    constraints = {
        'resource': 'Applications',
        'fields': [
            {'name': 'active', 'cardinality': {'mini': 0, 'maxi': '1'}},
            {'name': 'name', 'cardinality': {'mini': 0, 'maxi': '1'}},
            {'name': 'identifier', 'cardinality': {'mini': 0, 'maxi': '*'}}
        ]
    }

    with pytest.raises(Exception) as execinfo:
        org_profile = ResourceProfile(constraints)
        org_profile.apply_constraints()
    assert "Missing Resource" in str(execinfo.value)


def test_apply_constraints_with_field_names_not_in_resource():
    constraints = {
        'resource': 'Organization',
        'fields': [
            {'name': 'notafield', 'cardinality': {'mini': 0, 'maxi': '1'}},
            {'name': 'name', 'cardinality': {'mini': 0, 'maxi': '*'}},
        ]
    }

    org_profile = ResourceProfile(constraints)
    DemoOrgResource = org_profile.apply_constraints()
    assert DemoOrgResource.__tablename__ == 'Organization'


def test_xml_profile_manager_generates_dict():
    file_path = '/profiles/gawana-default.structuredefinition.xml'
    cls_inst = XMLProfileManager(BASE_DIR + file_path)
    constraints = cls_inst.construct_constraints()

    assert isinstance(constraints, dict)


def test_xml_profile_manager_generates_required_constraints():
    file_path = '/profiles/gawana-default.structuredefinition.xml'
    cls_inst = XMLProfileManager(BASE_DIR + file_path)
    constraints = cls_inst.construct_constraints()

    assert constraints['resource'] == 'Organization'

    # TODO Complete the test assertions defined below
    # data = {'cardinality': {'mini': '1', 'maxi': '1'}, 'name': 'name'}
    # assert str(data) in str(constraints)


def test_resource_profile_with_constraints_from_xml():
    file_path = '/profiles/gawana-default.structuredefinition.xml'
    cls_inst = XMLProfileManager(BASE_DIR + file_path)
    constraints = cls_inst.construct_constraints()

    org_profile = ResourceProfile(constraints)
    DemoOrgResource = org_profile.apply_constraints()
    assert DemoOrgResource.__tablename__ == 'Organization'
