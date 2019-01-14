from sqlalchemy_utils import CompositeType, CompositeArray
from sqlalchemy.types import TypeDecorator

from .cplxtype_validator import CompositeValidator


class PgComposite(CompositeType):
    """A composite type that creates a postgresql composite type field.

    Usage
    ^^^^^

    ::
        from sqlalchemy.types import Integer, Column, String
        from complex_mixin import PgComposite

        class ComplexTypes(db.Model):
            __tablename__ = 'complex_model'

            id = Column(Integer, primary_key=True)
            balance = Column(CompositeType(
                'new_type',
                [
                    Column('name', String, nullable=False),
                    Column('amount', Integer, nullable=True)
                    Column('status', String)
                ]
            ))

    Accessing fields
    ^^^^^^^^^^^^^^^^

    ::
        session.query(complex_model).filter(complex_model.balance.amount > 500)

    Populating Data
    ^^^^^^^^^^^^^^^

    ::
        data = ComplexTypes(
            id=12, balance={'amount': 200, 'name': 'test', 'status': 'paid'})

    Extends:
        CompositeType from sqlalchemy_utils
        http://sqlalchemy-utils.readthedocs.org/en/latest/
    """

    def copy(self):
        """Produce a copy of this :class:`.PgComposite` instance.

        This is a simple shallow copy implementation.
        """

        instance = self.__class__.__new__(self.__class__)
        instance.__dict__.update(self.__dict__)
        return instance

    def validate_col_data(self, values):
        cols = []
        for col in self.columns:
            if isinstance(col.type, PgComposite):
                cols.append(col)
        CompositeValidator(self.name, cols, values)
        return values

    def nested_composite_array(self, column, values):
        """compose a nested composite array type with values"""
        if not isinstance(column.type.item_type, PgComposite):
            return values

        if values is None:
            return None

        fields = {col.name: col for col in column.type.item_type.columns}
        new_value = []
        for field, data in fields.items():
            for i, val in enumerate(values):
                if isinstance(values[i], tuple):
                    values[i] = dict(values[i]._asdict())

                if values[i]:  # pragma: no cover
                    if not (field in values[i].keys()):
                        values[i][field] = None

                if isinstance(data.type, PgComposite):  # pragma: no cover
                    values[i][field] = self.nested_composite(data, values[i][field])

        # for val in values:
        for i, val in enumerate(values):
            if val:
                for k, v in enumerate(val):
                    if isinstance(val[v], list):
                        # Added for list objects that are nested within a
                        # complex element nested in a list of complex elements
                        # e.g Patient -> Contact[] -> relationship[] -> coding[]
                        col_type = fields[v]
                        val[v] = self.nested_composite_array(col_type, val[v])

            if values[i]:  # pragma: no cover
                new_value.append(column.type.item_type.type_cls(**values[i]))

        if len(new_value) > 0:  # pragma: no cover
            new_value = new_value
        else:  # pragma: no cover
            new_value = None

        return new_value

    def nested_composite(self, column, values):
        """compose a nested composite type with values"""

        if values is None:
            return None

        fields = {col.name: col for col in column.type.columns}
        for field, data in fields.items():
            if not (field in values.keys()):
                values[field] = None

            if isinstance(data.type, CompositeArray):
                values[field] = self.nested_composite_array(data, values[field])

            elif isinstance(data.type, PgComposite):
                values[field] = self.nested_composite(data, values[field])
        return (column.type).type_cls(**values)

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None

            new_value = []
            processed_value = []
            errors = []
            for i, column in enumerate(self.columns):
                try:
                    if isinstance(value, dict):
                        new_value.append(value[column.name])

                    else:
                        new_value.append(getattr(value, column.name))
                except Exception:
                    # VALIDATE IF NULLABLE IS TRUE OR FALSE
                    if not (column.nullable):
                        errors.append(
                            "Field %s in column %s not nullable"
                            % (column.name, self.name)
                        )
                    new_value.append(None)

                if isinstance(column.type, TypeDecorator):
                    processed_value.append(
                        column.type.process_bind_param(new_value[i], dialect)
                    )
                elif isinstance(column.type, PgComposite):
                    val = self.nested_composite(column, new_value[i])
                    processed_value.append(val)

                elif isinstance(column.type, CompositeArray):
                    val = self.nested_composite_array(column, new_value[i])
                    processed_value.append(val)

                else:
                    processed_value.append(new_value[i])

            if len(errors) > 0:
                raise ValueError(errors)

            result = self.validate_col_data(self.type_cls(*processed_value))
            return result

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is None:
                return None
            cls = value.__class__
            kwargs = {}
            for column in self.columns:
                if isinstance(column.type, TypeDecorator):
                    kwargs[column.name] = column.type.process_result_value(
                        getattr(value, column.name), dialect
                    )
                else:
                    kwargs[column.name] = getattr(value, column.name)
            return cls(**kwargs)

        return process
