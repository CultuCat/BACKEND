from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Tag

class SpaceViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tag1 = Tag.objects.create(nom="Tag 1")
        self.tag2 = Tag.objects.create(nom="Tag 2")

    def test_list_tags(self):
        response = self.client.get('/tags/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)