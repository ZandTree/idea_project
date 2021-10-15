from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from profiles.models import Profile

User = get_user_model()


class ProfileSerializerTestCase(APITestCase):
    """(C*)RUD operations around given profile object"""

    def setUp(self):
        self.user1 = User.objects.create(username="nick", email="zoo@mail.com")
        self.user2 = User.objects.create(username="jane", email="daspy@mail.com")
        self.user_staff = User.objects.create(username="boss", email="mystaff@mail.com", is_staff=True)

        self.profile = Profile.objects.filter(user_id=self.user1.id).last()
        self.profile.website = "http://www.havefun.com"
        self.profile.save()

    # ################## GET <=> READ PROFILE-INFO ##########################################################

    def test_get_single_profile_owner(self):
        """ user profile owner can READ profile"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('profile-owner', kwargs={"unid": self.user1.profile.unid})
        print("EXAMOLE PROFFILE URL", url)
        response = self.client.get(url)
        serial_profile = ProfileSerializer(self.profile).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serial_profile)

    def test_get_single_profile_staff(self):
        """ user staff can READ profile of others"""
        self.client.force_authenticate(user=self.user_staff)
        url = reverse('profile-owner', kwargs={"unid": self.user1.profile.unid})
        response = self.client.get(url)
        serial_profile = ProfileSerializer(self.profile).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serial_profile)

    def test_get_profile_by_not_owner(self):
        """ user NOT profile owner can't READ profile"""
        self.client.force_authenticate(user=self.user2)
        url = reverse('profile-owner', kwargs={"unid": self.user1.profile.unid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # # ################### DELETE #############################################

    def test_delete_profile_by_owner(self):
        """ user profile owner can DELETE his profile"""
        start_count = Profile.objects.count()
        self.client.force_authenticate(user=self.user1)
        url = reverse('profile-owner', kwargs={"unid": self.user1.profile.unid})
        resp = self.client.delete(url)
        final_count = Profile.objects.count()
        self.assertEqual(resp.status_code, 204)
        self.assertNotEqual(start_count, final_count)

    def test_delete_profile_by_staff(self):
        """ user staff can DELETE given profile"""
        start_count = Profile.objects.count()
        self.client.force_authenticate(user=self.user_staff)
        url = reverse('profile-owner', kwargs={"unid": self.user1.profile.unid})
        resp = self.client.delete(url)
        final_count = Profile.objects.count()
        self.assertEqual(resp.status_code, 204)
        self.assertNotEqual(start_count, final_count)

    def test_delete_profile_by_not_owner(self):
        """ user = !profile owner can't  DELETE profile of others"""
        start_count = Profile.objects.count()
        self.client.force_authenticate(user=self.user2)
        url = reverse('profile-owner', kwargs={"unid": self.user1.profile.unid})
        resp = self.client.delete(url)
        final_count = Profile.objects.count()
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(start_count, final_count)

    ################### UPDATE <=> PUT ##################################
    def test_put_update_profile(self):
        """ user == owner of the profile can change his profile"""
        self.client.force_authenticate(user=self.user1)
        initial_website = self.profile.website
        url = reverse('profile-owner', kwargs={"unid": self.user1.profile.unid})
        print("line 91 url", url)
        modified_profile = {
            "website": "http://www.jane.web-site.com"
        }

        content = encode_multipart('BoUnDaRyStRiNg', modified_profile)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        resp = self.client.put(url, content, content_type=content_type)
        modified_website = resp.data['website']
        self.profile.refresh_from_db()
        self.user1.refresh_from_db()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertNotEqual(initial_website, modified_website)

    def test_put_update_profile(self):
        """ user == profile owner gets error if link broken"""
        self.client.force_authenticate(user=self.user1)
        initial_website = self.profile.website
        url = reverse('profile-owner', kwargs={"unid": self.user1.profile.unid})
        modified_profile = {
            "website": "httpwww.fhfhhf.com"
        }
        content = encode_multipart('BoUnDaRyStRiNg', modified_profile)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        resp = self.client.put(url, content, content_type=content_type)
        modified_website = resp.data['website']
        self.profile.refresh_from_db()
        self.user1.refresh_from_db()
        self.assertEqual(resp.status_code, 400)
        self.assertNotEqual(initial_website, modified_website)

    def test_put_update_profile_not_owner(self):
        """ user not owner of given profile CAN'T CHANGE the profile"""
        self.client.force_authenticate(user=self.user2)
        url = reverse('profile-owner', kwargs={"unid": self.user1.profile.unid})
        initial_profile_website = self.profile.website
        modified_profile = {
            "website": "https://boze-wolf-user.com"

        }
        content = encode_multipart('BoUnDaRyStRiNg', modified_profile)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        resp = self.client.put(url, content, content_type=content_type)
        # json_edited_idea = json.dumps(modified_profile)
        # resp = self.client.put(url, data=json_edited_idea, content_type='application/json')
        self.profile.refresh_from_db()
        self.user1.refresh_from_db()
        self.assertEqual(initial_profile_website, self.profile.website)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_update_profile_staff(self):
        """ user == staff can change any profile"""
        self.client.force_authenticate(user=self.user_staff)
        url = reverse('profile-owner', kwargs={"unid": self.user1.profile.unid})
        print("line 145 url is", url)
        modified_profile = {
            "website": "https://www.linked-in/help-for-my-user-site.com",

        }

        content = encode_multipart('BoUnDaRyStRiNg', modified_profile)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        resp = self.client.put(url, content, content_type=content_type)
        # json_edited_idea = json.dumps(modified_profile)
        # resp = self.client.put(url, data=json_edited_idea, content_type='application/json')
        self.profile.refresh_from_db()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
