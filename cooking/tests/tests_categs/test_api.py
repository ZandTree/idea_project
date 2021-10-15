from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from ideas.models import Idea, Category
from api.serializers.categs.categ_ser import CategorySerializer
from api.serializers.ideas.idea_ser import IdeaSerializer

User = get_user_model()


class CategTestCase(APITestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name="chat")
        self.category2 = Category.objects.create(name="kletskoek")
        self.category3 = Category.objects.create(name="talk", parent=self.category2)
        self.category4 = Category.objects.create(name="ha-ha", parent=self.category3)
        self.category5 = Category.objects.create(name="zoo", parent=self.category4)

        self.user1 = User.objects.create(username="jane", email="zoo@mail.com", password="viola34")
        self.user2 = User.objects.create(username="kate", email="giraf@mail.com", password="yahoo34")
        self.idea1 = Idea.objects.create(
            title="first idea",
            author=self.user1,
            categ=self.category1,
            lead_text="Greet 1",
            main_text="Main text one"
        )
        self.idea2 = Idea.objects.create(
            title="second idea",
            author=self.user1,
            categ=self.category1,
            lead_text="Greet 2",
            main_text="Main text two"
        )
        self.idea3 = Idea.objects.create(
            title="third idea time",
            author=self.user2,
            categ=self.category2,
            lead_text="User 2 is great",
            main_text="Main text user2"

        )
        self.idea4 = Idea.objects.create(
            title="fourth  time",
            author=self.user2,
            categ=self.category3,
            lead_text="Summer day",
            main_text="Main text from user2"

        )
        self.cats = Category.objects.all()

    # important note:set pagination class in settings: should be None and work with length qs

    def test_get_all_ideas(self):
        """set pagination class in viewset ideas: should be None"""
        url = reverse('category-list')
        response = self.client.get(url)
        local_serialized_data = CategorySerializer(self.cats, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(local_serialized_data, response.data)

    def test_get_idea_for_category_without_children(self):
        url = reverse('cat-per-idea', kwargs={"slug": self.category1.slug})
        response = self.client.get(url)
        local_serialized_data = IdeaSerializer(self.category1.ideas.all(), many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)
        self.assertEqual(len(local_serialized_data), 2)

    def test_get_ideas_for_given_category_incl_descendants(self):
        """ let op: here OrderDict with key='count' otherwise 
        comment pagination in settings
        exp result (ideas for categ and ideas of it's descendants (categ3))
        """
        url = reverse('cat-per-idea', kwargs={"slug": self.category2.slug})
        response = self.client.get(url)
        local_collection = IdeaSerializer([self.idea3, self.idea4], many=True).data
        self.assertEqual(response.data.get('count'), len(local_collection))
        self.assertEqual(response.status_code, 200)

    def test_get_404_for_not_existed_category(self):
        url = reverse('cat-per-idea', kwargs={"slug": "hghghghghghutut123"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
