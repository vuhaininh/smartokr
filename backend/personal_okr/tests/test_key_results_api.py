from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from personal_okr.models import KeyResult, Objective
from personal_okr.serializers import KeyResultSerializer
from faker import Faker
fake = Faker()

KEY_RESULT_URL = reverse('personal_okr:keyresult-list')


def sample_user(**params):
    defaults = {
        'email': fake.email(),
        'password': 'testpassword'
    }
    defaults.update(params)
    return get_user_model().objects.create(**defaults)


def sample_key_result(user, objective, **params):
    """Create and return a sample key result"""
    defaults = {
        'description': fake.sentences(nb=1, ext_word_list=None),
        'finished_date': fake.date(pattern="%Y-%m-%d", end_datetime=None)
    }
    defaults.update(params)
    return KeyResult.objects.create(user=user, objective=objective, **defaults)


def sample_objective(user, **params):
    """Create and return a sample objective"""
    defaults = {
        'description': fake.sentences(nb=1, ext_word_list=None),
        'finished_date': fake.date(pattern="%Y-%m-%d", end_datetime=None)
    }
    defaults.update(params)
    return Objective.objects.create(user=user, **defaults)


class PublicKeyResultApiTests(TestCase):
    """Test unauthenticated Key Result Api access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(KEY_RESULT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateKeyResultApiTests(TestCase):
    """Test unauthenticated key result API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_key_results(self):
        """Test retrieving a list of key results"""
        objective = sample_objective(self.user)
        sample_key_result(self.user, objective)
        sample_key_result(self.user, objective)
        key_results = KeyResult.objects.filter(
            user=self.user, objective=objective).order_by('-id')
        serializer = KeyResultSerializer(key_results, many=True)

        res = self.client.get(KEY_RESULT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_key_results_limited_to_user(self):
        """Test retrieving key results for user"""
        user2 = get_user_model().objects.create_user(
            fake.email(),
            'samplepass'
        )
        objective2 = sample_objective(user2)
        sample_key_result(user2, objective2)
        objective = sample_objective(self.user)
        sample_key_result(self.user, objective)
        res = self.client.get(KEY_RESULT_URL)

        key_results = KeyResult.objects.filter(user=self.user)
        serializer = KeyResultSerializer(key_results, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
