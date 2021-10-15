from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.test.client import encode_multipart

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import ErrorDetail
from ideas.models import Idea, Category, UserIdeaRelation

from api.serializers.ideas.idea_ser import IdeaSerializer

User = get_user_model()


class IdeaTestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="chat")
        # url = 'http://127.0.0.1:8000/auth/jwt/create/'
        self.user1 = User.objects.create(username="snork", email="zoo@mail.com", password="viola34")
        self.user2 = User.objects.create(username="hemul", email="giraf@mail.com", password="yahoo34")

        self.idea1 = Idea.objects.create(
            title="first idea",
            author=self.user1,
            categ=self.category,
            lead_text="Greet 1",
            main_text="Main text one",
            featured=True
        )

        self.idea1.tags.add("first", "second")

        self.idea2 = Idea.objects.create(
            title="second idea",
            author=self.user1,
            categ=self.category,
            lead_text="Holiday great",
            main_text="Main text two",
            featured=True,

        )
        self.idea2.tags.add("era")

        self.idea3 = Idea.objects.create(
            title="summer time",
            author=self.user2,
            categ=self.category,
            lead_text="User 2 is great",
            main_text="Main text user2"

        )
        self.useridearelation = UserIdeaRelation.objects.create(
            user=self.user2,
            idea=self.idea1,
            like=True,
            rating=5

        )
        self.ideas = Idea.objects.annotate(
            users_comments=Count('comments', distinct=True)
        ).order_by('-created_at')

    def test_create_idea(self):
        """in setUp idea (author == req.user);
        let op: Newer Django has a immutable QueryDict,
        |=> setattr(request.data, '_mutable', True) in viewset .create
        """
        self.assertEqual(3, Idea.objects.all().count())
        url = reverse('idea-list')
        self.client.force_authenticate(user=self.user1)
        new_idea = {
            "title": "great lake",
            "lead_text": "greet from woods",
            "categ": self.category.id,
            "main_text": "test it again",
            "featured": True,
            "tags": ["zoo"]

        }
        content = encode_multipart('BoUnDaRyStRiNg', new_idea)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        response = self.client.post(url, content, content_type=content_type)
        author_new_idea = Idea.objects.last().author
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(4, Idea.objects.all().count())
        self.assertEqual(self.user1, author_new_idea)

    def test_get_all_ideas(self):
        """ let op:postgresql with comments vs serMethodField(sqlite3) """
        # ideas = Idea.objects.all()
        # annotate(an_likes=Count(Case(When(useridearelation__like=True, then=1))))
        url = reverse('idea-list')
        response = self.client.get(url)
        local_serialized_data = IdeaSerializer(self.ideas, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(local_serialized_data, response.data)

    def test_get_one_idea(self):
        url = reverse('idea-detail', kwargs={"slug": self.idea1.slug})
        response = self.client.get(url)
        local_serialized_data = IdeaSerializer(self.ideas.filter(id=self.idea1.id).last()).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(local_serialized_data, response.data)
        self.assertEqual(local_serialized_data['featured'], True)
        self.assertEqual(local_serialized_data['avg_rate'], '5.00')
        self.assertEqual(len(local_serialized_data['tags']), 2)

    def test_create_idea_valid_tags(self):
        """in setUp idea (author == req.user);
        let op: Newer Django has a immutable QueryDict,
        |=> setattr(request.data, '_mutable', True) in viewset .create
        """
        self.assertEqual(3, Idea.objects.all().count())
        url = reverse('idea-list')
        self.client.force_authenticate(user=self.user1)

        new_idea = {
            "title": "to delete",
            "lead_text": "greet testsn",
            "categ": self.category.id,
            "main_text": "test it again",
            # should be a list with a string ["item1,item2"]
            "tags": ["foo,bar"]
        }

        content = encode_multipart('BoUnDaRyStRiNg', new_idea)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        response = self.client.post(url, content, content_type=content_type)

        author_new_idea = Idea.objects.last().author

        new_idea = Idea.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(4, Idea.objects.all().count())
        self.assertEqual(self.user1, author_new_idea)
        self.assertEqual(new_idea.tags.count(), 2)
        self.assertEqual(len(response.data['tags']), 2)

    def test_create_idea_invalid_tags(self):
        """in setUp idea (author == req.user);
        let op: Newer Django has a immutable QueryDict,
        |=> setattr(request.data, '_mutable', True) in viewset .create
        """
        self.assertEqual(3, Idea.objects.all().count())
        url = reverse('idea-list')
        self.client.force_authenticate(user=self.user1)
        print("user is auth-ed", self.user1)
        new_idea = {
            "title": "to delete",
            "lead_text": "greet testsn",
            "categ": self.category.id,
            "main_text": "test it again",
            "tags": ["foo,bar,ghghgh,jgjgjgjjg,99999,ghhhhhhhhhhh,ytytytyt"]

        }

        content = encode_multipart('BoUnDaRyStRiNg', new_idea)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        response = self.client.post(url, content, content_type=content_type)
        serv_data_detail_err = response.data.get('detail')
        self.assertEqual(response.status_code, 400)
        self.assertTrue(serv_data_detail_err)
        self.assertEqual(3, Idea.objects.all().count())

    def test_put_update_idea(self):
        """in setUp idea (user is auth-ed; author == req.user)"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('idea-detail', args=(self.idea2.slug,))
        featured_ideas_count_init = Idea.objects.filter(featured=True).count()
        initial_tags = self.idea2.tags.all()
        modified_idea = {
            "title": "second idea modified",
            "author": self.user1.id,
            "categ": self.category.id,
            "lead_text": "Greet 2 modified",
            "main_text": "Modified Main text two",
            "featured": False,
            "tags": ["zaja tio,was"]

        }
        content = encode_multipart('BoUnDaRyStRiNg', modified_idea)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        resp = self.client.put(url, content, content_type=content_type)
        featured_ideas_count_finish = Idea.objects.filter(featured=True).count()
        final_tags = self.idea2.tags.all()
        self.idea2.refresh_from_db()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.idea2.lead_text, "Greet 2 modified")
        self.assertEqual(self.idea2.featured, False)
        self.assertNotEqual(featured_ideas_count_init, featured_ideas_count_finish)
        self.assertEqual(1, featured_ideas_count_finish)
        self.assertEqual(self.idea2.tags.count(), 2)
        self.assertNotEqual(initial_tags, final_tags)
        self.assertEqual(initial_tags.filter(name='zaja tio').exists(), True)
        self.assertEqual(initial_tags.filter(slug='zaja-tio').exists(), True)
        self.assertEqual(initial_tags.filter(name='was').exists(), True)

    def test_put_update_idea_not_author(self):
        """ Important to add:  user is auth-ed but not the author of the idea)"""
        self.client.force_authenticate(user=self.user2)
        url = reverse('idea-detail', args=(self.idea2.slug,))

        modified_idea = {
            "title": "second idea modified",
            "author": self.user1.id,
            "categ": self.category.id,
            "lead_text": "Greet 2 modified",
            "main_text": "Main text two"

        }
        content = encode_multipart('BoUnDaRyStRiNg', modified_idea)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        resp = self.client.put(url, content, content_type=content_type)
        self.idea2.refresh_from_db()
        error_msg = {'detail': ErrorDetail(
            string='You do not have permission to perform this action.', code='permission_denied')}

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.idea2.lead_text, "Holiday great")
        self.assertEqual(resp.data, error_msg)

    def test_delete_idea(self):
        """author of the idea == req.user can DELETE his idea"""
        self.client.force_authenticate(user=self.user1)
        initial_count_ideas = Idea.objects.count()
        url = reverse('idea-detail', args=(self.idea2.slug,))
        resp = self.client.delete(url)
        final_count_ideas = Idea.objects.count()
        self.assertEqual(resp.status_code, 204)
        self.assertNotEqual(initial_count_ideas, final_count_ideas)

    def test_delete_idea_by_not_author(self):
        """auth-ed user but not author of the idea CAN'DELETE idea of others"""

        self.client.force_authenticate(user=self.user2)
        initial_count_ideas = Idea.objects.count()
        url = reverse('idea-detail', args=(self.idea2.slug,))
        resp = self.client.delete(url)
        final_count_ideas = Idea.objects.count()
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(initial_count_ideas, final_count_ideas)

    def test_delete_idea_by_staff(self):
        """staff can DELETE any idea"""
        self.user3 = User.objects.create(username="boo@faoo.com", is_staff=True)
        self.client.force_authenticate(user=self.user3)
        initial_count_ideas = Idea.objects.count()
        url = reverse('idea-detail', args=(self.idea2.slug,))
        resp = self.client.delete(url)
        final_count_ideas = Idea.objects.count()
        self.assertNotEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(resp.status_code, 204)
        self.assertNotEqual(initial_count_ideas, final_count_ideas)
        self.assertEqual(2, final_count_ideas)


class IdeaApiSearchOrderingTestCase(APITestCase):
    """ let op: postgresql vs sqlite3 users_comments"""

    def setUp(self) -> None:
        self.category = Category.objects.create(name="chat")
        self.user1 = User.objects.create(username="rio", email="zoo@mail.com")
        self.idea1 = Idea.objects.create(
            title="first idea rio",
            author=self.user1,
            categ=self.category,
            lead_text="Greet 1",
            main_text="Main text one",
            featured=True,
            status=1
        )
        self.idea2 = Idea.objects.create(
            title="second idea",
            author=self.user1,
            categ=self.category,
            lead_text="Greet 2 rio",
            main_text="Main text two",
            status=1
        )
        self.idea3 = Idea.objects.create(
            title="third idea",
            author=self.user1,
            categ=self.category,
            lead_text="Greet 3 ",
            main_text="Main text three rio",
            status=2
        )

    def test_get_search(self):
        """
        search: test to catch word in title/lead_text/main_text
        """
        ideas = Idea.objects.annotate(
            users_comments=Count('comments', distinct=True)).filter(
            id__in=(self.idea1.id, self.idea2.id, self.idea3.id)).order_by('-created_at')
        url = reverse('idea-list')
        serializer_data = IdeaSerializer(ideas, many=True).data
        resp = self.client.get(url, data={"search": "rio"})

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, resp.data)
        self.assertEqual(len(serializer_data), 3)

    def test_get_order_oldest_on_top(self):
        """
        search: test to get filter for status;
        """
        ideas = Idea.objects.annotate(
            users_comments=Count('comments', distinct=True)).filter(
            id__in=(self.idea3.id, self.idea2.id, self.idea1.id)).order_by('-created_at')
        url = reverse('idea-list')
        serializer_data = IdeaSerializer(ideas, many=True).data
        resp = self.client.get(url, data={"ordering": "-created_at"})
        first_the_oldest = resp.data[0]['title']
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, resp.data)
        self.assertEqual(first_the_oldest, self.idea3.title)
