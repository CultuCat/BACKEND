from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Space

class SpaceViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.space1 = Space.objects.create(nom="Space 1", latitud=40.7128, longitud=-74.0060)
        self.space2 = Space.objects.create(nom="Space 2", latitud=34.0522, longitud=-118.2437)

    def test_list_spaces(self):
        response = self.client.get('/spaces/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_spaces_by_distance(self):
        data = {
            'latitud': 40.7128,
            'longitud': -74.0060,
            'num_objs': 50
        }
        response = self.client.get('/spaces/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

