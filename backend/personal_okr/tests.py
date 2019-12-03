from django.test import TestCase
from personal_okr.views import add
# Create your tests here.


class ViewsTests(TestCase):

    def test_add_numbers(self):
        """"Test that 2 numbers added together"""
        self.assertEqual(add(3, 8), 11)
