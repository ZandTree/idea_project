from django.test import TestCase
from django.contrib.auth import get_user_model
from api.serializers.account.user_serializer import UserSerializer
from profiles.models import Profile

User = get_user_model()


class UserSerializerTestCase(TestCase):
    """compare expected and received data after ser-on"""

    def setUp(self):
        self.user = User.objects.create(username="jane", email="zoo@mail.com")
        self.profile = Profile.objects.last()

    def test_user_serializer(self):
        """ check weather user info comes with his profile """
        serial_user = UserSerializer(self.user).data
        expected_data = {
            "id": self.user.id,
            "username": self.user.username,
            "unid": self.profile.unid

        }
        self.assertEqual(serial_user, expected_data)
