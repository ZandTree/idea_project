from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ideas.models import UserIdeaRelation, Idea, Category
from ideas.logic import calc_rating, calc_count_likes, calc_max_rating

User = get_user_model()


class IdeaTestCase(APITestCase):
    """
    test only of postgres
    """

    def setUp(self):
        self.category = Category.objects.create(name="chat")
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
        self.idea2 = Idea.objects.create(
            title="second idea",
            author=self.user1,
            categ=self.category,
            lead_text="Holiday great",
            main_text="Main text two",
            featured=True,
        )
        self.idea3 = Idea.objects.create(
            title="summer time",
            author=self.user2,
            categ=self.category,
            lead_text="User 2 is great",
            main_text="Main text user2"
        )
        self.useridearelation1 = UserIdeaRelation.objects.create(
            user=self.user2,
            idea=self.idea1,
            like=True,
            rating=5
        )
        self.useridearelation2 = UserIdeaRelation.objects.create(
            user=self.user2,
            idea=self.idea1,
            like=True,
            rating=2
        )
        self.useridearelation3 = UserIdeaRelation.objects.create(
            user=self.user2,
            idea=self.idea1,

        )

        self.ideas = Idea.objects.order_by('-created_at')
        self.idea1 = self.ideas.get(id=self.idea1.id)

    def test_calc_rating(self):
        calc_rating(self.idea1)
        self.idea1.refresh_from_db()
        self.assertEqual('3.50', str(self.idea1.avg_rate))

    def test_calc_count_likes(self):
        calc_count_likes(self.idea1)
        self.idea1.refresh_from_db()
        self.assertEqual(2, self.idea1.an_likes)

    def test_calc_max_rating(self):
        calc_max_rating(self.idea1)
        self.idea1.refresh_from_db()
        self.assertEqual(5, self.idea1.max_rating)
