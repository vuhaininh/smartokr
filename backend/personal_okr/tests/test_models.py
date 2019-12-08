from django.test import TestCase
from django.contrib.auth import get_user_model
from personal_okr import models


def sample_user(email='test@devapp.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_objective_str(self):
        """Test the objective string representation"""
        objective = models.Objective.objects.create(
            user=sample_user(),
            description="Improve the customer service",
            finished_date='2019-11-20'
        )
        self.assertEqual(str(objective), objective.description)
