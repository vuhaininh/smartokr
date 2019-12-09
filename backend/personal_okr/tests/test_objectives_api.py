from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from personal_okr.models import Objective
from personal_okr.serializers import ObjectiveSerializer

OBJECTIVES_URL = reverse('personal_okr:objective-list')


class PublicObjectivesApiTests(TestCase):
    """ Test the publicly available objectives API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint """
        res = self.client.get(OBJECTIVES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateObjectivesApiTests(TestCase):
    """Test the private objectives API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@testapp.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_objective_list(self):
        """Test retrieving a list of objectives"""
        Objective.objects.create(
            user=self.user, description="Finish Backend API",
            finished_date="2019-08-28")
        Objective.objects.create(
            user=self.user, description="Finish Frontend React",
            finished_date="2019-11-20"
        )
        res = self.client.get(OBJECTIVES_URL)
        objectives = Objective.objects.all().order_by('-description')
        serializer = ObjectiveSerializer(objectives, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_objectives_limited_to_user(self):
        """Test that objecties for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@testapp.com',
            'testpassword'
        )
        Objective.objects.create(user=user2, description='Test Ikigai OKR app',
                                 finished_date='2020-01-01')
        objective = Objective.objects.create(user=self.user,
                                             description='Test React App',
                                             finished_date='2020-02-02')
        res = self.client.get(OBJECTIVES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['description'], objective.description)

    def test_create_objective_successful(self):
        """Test create a new objective"""
        payload = {'description': 'Test Description',
                   'finished_date': '2020-01-01'}
        self.client.post(OBJECTIVES_URL, payload)
        exists = Objective.objects.filter(
            user=self.user,
            description=payload['description'],
            finished_date=payload['finished_date'],
        ).exists()

        self.assertTrue(exists)

    def test_create_objective_invalid(self):
        """Test creating invalid objective fails"""
        payload = {'description': ''}
        res = self.client.post(OBJECTIVES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
