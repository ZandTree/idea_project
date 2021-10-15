from django.test import TestCase
from django.db.models import When, Case, Count, Avg
from django.contrib.auth import get_user_model

from ideas.models import Idea, Category, UserIdeaRelation

from api.serializers.ideas.idea_test_ser import IdeaTestSerializer

User = get_user_model()


#
# tests for post gresql
class IdeaTestSerializerTesCase(TestCase):
    """ note: had to dismiss created_at field for the purpose of testing"""

    def setUp(self):
        self.category = Category.objects.create(name="chat")
        self.user1 = User.objects.create(username="jane", email="zoo@mail.com")
        self.user2 = User.objects.create(username="nick", email="zoo2@mail.com")
        self.user3 = User.objects.create(username="kate", email="zoo3@mail.com")
        self.idea1 = Idea.objects.create(
            title="first idea",
            author=self.user1,
            categ=self.category,
            lead_text="Greet 1",
            main_text="Main text one",
            status=1

        )
        self.idea1.tags.add("zoo")

        self.idea2 = Idea.objects.create(
            title="second idea",
            author=self.user1,
            categ=self.category,
            lead_text="Greet 2",
            main_text="Main text two",
            featured=True

        )
        self.idea2.tags.add("mio")

        self.user_idea_rel1 = UserIdeaRelation.objects.create(
            idea=self.idea1,
            user=self.user1,
            like=True,
            rating=5
        )
        self.user_idea_rel2 = UserIdeaRelation.objects.create(
            idea=self.idea1,
            user=self.user2,
            like=True,
            rating=3
        )
        self.user_idea_rel3 = UserIdeaRelation.objects.create(
            idea=self.idea1,
            user=self.user3,
            like=True
        )
        self.user_idea_rel4 = UserIdeaRelation.objects.create(
            idea=self.idea2,
            user=self.user3,
            like=True,
            rating=5
        )
        self.user_idea_rel5 = UserIdeaRelation.objects.create(
            idea=self.idea2,
            user=self.user1,
            like=False,
            rating=2
        )
        self.user_idea_rel6 = UserIdeaRelation.objects.create(
            idea=self.idea2,
            user=self.user2,
            rating=3,
            like=False
        )

        self.ideas = Idea.objects.select_related('author', 'categ').prefetch_related('tags').order_by('created_at')

    def test_idea_serializer(self):
        serial_ideas = IdeaTestSerializer(self.ideas, many=True).data
        print(serial_ideas)
        expected_data = [
            {"id": self.idea1.id,
             "slug": self.idea1.slug,
             "title": "first idea",
             "author": self.user1.id,
             "lead_text": "Greet 1",
             "categ": self.category.id,
             "categ_name": self.category.name,
             "main_text": "Main text one",
             "owner_idea": self.user1.username,
             "status": 1,
             "an_likes": 3,
             "avg_rate": '4.00',
             "featured": False,
             "tags": ["zoo"],
             },

            {"id": self.idea2.id,
             "slug": self.idea2.slug,
             "title": "second idea",
             "author": self.user1.id,
             "lead_text": "Greet 2",
             "categ_name": self.category.name,
             "categ": self.category.id,
             "main_text": "Main text two",
             "owner_idea": self.user1.username,
             "status": 0,
             "an_likes": 1,
             "avg_rate": '3.33',
             "featured": True,
             "tags": ["mio"]}
        ]

        self.assertEqual(serial_ideas, expected_data)
