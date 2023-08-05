class ServiceBase:
    pass


# integrating django model ----------------------------------
try:
    from django.core.exceptions import ValidationError
    from django.db import models as types

except ImportError:
    class Service (ServiceBase):
        pass

else:
    import datetime
    import uuid
    from rs4.attrdict import AttrDict

    TYPE_MAP = [
        (types.CharField, str, 'string'),
        ((types.IntegerField, types.AutoField), int, 'integer'),
        (types.FloatField, float, 'float'),
        (types.BooleanField, bool, 'boolean'),
        (types.DateTimeField, datetime.datetime, 'datetime'),
        (types.DateField, datetime.date, 'date'),
        (types.TimeField, datetime.time, 'string'),
        (types.UUIDField, uuid.UUID, 'uuid'),
    ]

    class TableInfo:
        def __init__ (self, name, columns):
            self.name = name
            self.columns = columns

        def __getitem__ (self, k):
            return self.columns [k]


    class Service (ServiceBase):
        ValidationError = ValidationError

        @classmethod
        def get_table_info (cls, model):
            return TableInfo (cls.get_table_name (model), cls.get_table_columns (model))

        @classmethod
        def get_table_name (cls, model):
            return model._meta.db_table

        @classmethod
        def get_table_columns (cls, model):
            columns = {}
            for field in model._meta.fields:
                field_type = None
                for ftype, ptype, name in TYPE_MAP:
                    if isinstance (field, ftype):
                        field_type = ptype
                        break
                columns [field.column] = AttrDict (dict (
                    column = field.column,
                    type = field_type,
                    pk = field.primary_key,
                    unique = field.unique,
                    max_length = field.max_length,
                    null = field.null,
                    blank = field.blank,
                    choices = field.choices,
                    help_text = field.help_text
                ))
            return columns

        @classmethod
        def validate (cls, model, payload, null_check = False):
            fields = set ()
            for field in model._meta.fields:
                fields.add (field.column)
                if field.column not in payload:
                    if null_check and field.null is False:
                        raise ValidationError ('field {} is missing'.format (field.column))
                    continue

                value = payload [field.column]
                if field.null is False and value is None:
                    raise ValidationError ('field {} should not be NULL'.format (field.column))
                if field.blank is False and value == '':
                    raise ValidationError ('field {} should not be blank'.format (field.column))

                if value == '':
                    if not isinstance (field, types.CharField):
                        payload [field.column] = value = None
                if value is None:
                    return True

                for ftype, ptype, name in TYPE_MAP:
                    if isinstance (field, ftype) and not isinstance (value, ptype):
                        raise ValidationError ('field {} type should be {}'.format (field.column, name))

                if field.choices:
                    if isinstance (field.choices [0], (list, tuple)):
                        choices = [item [0] for item in field.choices]
                    else:
                        choices = field.choices
                    if value not in choices:
                        raise ValidationError ('field {} has invalid value'.format (field.column))

                if field.validators:
                    for validate_func in field.validators:
                        validate_func (value)

            for k in payload:
                if k not in fields:
                    raise ValidationError ('field {} is not valid field'.format (k))
