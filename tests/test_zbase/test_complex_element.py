import warnings

from fhir_server.elements import primitives
from fhir_server.elements.base.pg_types import register_pg_types
from fhir_server.elements.base.complex_element import (
    ComplexElement, Field, CompositeArray)


def test_extending_element_properties():
    arr = ComplexElement().element_properties()
    test_fields = [
        Field('end_time', {'mini': 0, 'maxi': 1},
              primitives.DateTimeField, None),

        Field('start_time', {'mini': 0, 'maxi': 1},
              primitives.DateTimeField, None)
    ]
    arr.extend(test_fields)

    assert arr == test_fields


def test_fhir_prefix_added_to_datatype():
    def some_datatype():
        class SomeType(ComplexElement):
            def element_properties(self):
                elm = super().element_properties()
                elm.extend([
                    Field('end_time', {'mini': 0, 'maxi': 1},
                          primitives.DateTimeField, None),

                    Field('start_time', {'mini': 0, 'maxi': 1},
                          primitives.DateTimeField, None)
                ])
                return elm
        return SomeType()

    fields = some_datatype()
    assert fields().name == 'fhir_sometype'


def test_default_extension_and_id_fields_added():
    def some_datatype():
        class SomeType(ComplexElement):
            def element_properties(self):
                elm = super().element_properties()
                elm.extend([
                    Field('end_time', {'mini': 0, 'maxi': 1},
                          primitives.DateTimeField, None)
                ])
                return elm
        return SomeType()

    fields = some_datatype()
    assert fields().columns[1].name == 'extension'
    assert fields().columns[0].name == 'id'


def test_one_to_many_fields():
    def some_datatype():
        class SomeType(ComplexElement):
            def element_properties(self):
                elm = super().element_properties()
                elm.extend([
                    Field('end_time', {'mini': 1, 'maxi': -1},
                          primitives.DateTimeField, None)
                ])
                return elm
        return SomeType()

    fields = some_datatype()
    assert fields().columns[2].nullable is False
    assert isinstance(fields().columns[2].type, CompositeArray)


def test_extending_element_properties_with_empty_fields():
    def some_datatype():
        class SomeType(ComplexElement):
            def element_properties(self):
                elm = super().element_properties()
                elm.extend([])
                return elm
        return SomeType()

    fields = some_datatype()
    assert len(fields().columns) == 2


def test_fails_to_create_duplicate_types(session):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        register_pg_types(session)
        assert len(w) == 1
        assert 'type "fhir_extension" already exists' in str(w[-1].message)
