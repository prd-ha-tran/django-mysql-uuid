import uuid

from django.test import TransactionTestCase

from tests.models import User, UserEmail


class TestSimple(TransactionTestCase):
    def test_insert(self):
        u = User(username="foo")
        u.save()
        u.refresh_from_db()
        UserEmail(user=u, email="foo@example.com").save()
        assert isinstance(u.guid, uuid.UUID)
        assert u.useremail_set.count() == 1
        assert isinstance(u.useremail_set.first().guid, uuid.UUID)
        example_uuid = uuid.uuid1()
        UserEmail(user=u, email="foo.baz@example.com", guid=example_uuid).save()
        assert u.useremail_set.last().guid == example_uuid

    def test_query(self):
        u = User(username="foo")
        u.save()
        assert User.objects.filter(guid=u.guid).count() == 1

    def test_bulk_create(self):
        users  = [User(username="foo"), User(username="baz")]
        User.objects.bulk_create(users)
        assert User.objects.count() == 2

    def test_invalid_uuid(self):
        u = User(username="foo")
        u.save()
        u.refresh_from_db()
        example_uuid = uuid.uuid4()
        with self.assertRaises(ValueError):
            UserEmail(user=u, email="foo@example.com", guid=example_uuid).save()
