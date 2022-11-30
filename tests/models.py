from django_mysql_uuid import OrderedUUIDField
from django.db.models import fields, Model, ForeignKey, CASCADE


class User(Model):
    guid = OrderedUUIDField(primary_key=True)
    username = fields.CharField(max_length=25)


class UserEmail(Model):
    user = ForeignKey(User, to_field="guid", on_delete=CASCADE)
    email = fields.EmailField()
    guid = OrderedUUIDField()
