import uuid

from django.db.models.fields import UUIDField, BinaryField
from django.utils.translation import gettext_lazy as _


def uuid_to_bin(val: uuid.UUID):
    hex_bytes = val.bytes
    return hex_bytes[6:8] + hex_bytes[4:6] + hex_bytes[0:4] + hex_bytes[8:16]


def bin_to_uuid(val: bytes):
    hex_bytes = val[4:8] + val[2:4] + val[0:2] + val[8:16]
    return uuid.UUID(bytes=hex_bytes)


class OrderedUUIDField(BinaryField):
    description = _("MySQL optimized UUID field.")
    empty_strings_allowed = False
    empty_values = [None]


    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 16
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def db_type(self, connection):
        return "binary(%s)" % self.max_length

    def get_default(self):
        if self.has_default() and not callable(self.default):
            return self.default
        default = super().get_default()
        if not default:
            return uuid.uuid1()
        return default

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        if not isinstance(value, uuid.UUID):
            value = self.to_python(value)
        if value.version != 1:
            raise ValueError("UUIDv1 must be used.")
        return connection.Database.Binary(uuid_to_bin(value))

    def to_python(self, value):
        return UUIDField.to_python(self, value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return bin_to_uuid(value)
