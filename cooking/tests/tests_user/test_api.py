from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

User = get_user_model()


class UserCreateDjoserSerializerTesCase(APITestCase):
    """return user info for djoser url='auth/users/me'"""

    def setUp(self):
        self.user1 = User.objects.create(username="jane", email="zoo@mail.com", password="12345")
        self.user2 = User.objects.create(username="jan", email="wood@mail.com", password="12345")

    def test_get_user(self):
        """ via djoser built-in view: get user"""
        self.client.force_authenticate(user=self.user1)
        url = '/auth/users/me'
        response = self.client.get(url)
        print("resp line 21", response)
        self.assertEqual(response.status_code, 200)
