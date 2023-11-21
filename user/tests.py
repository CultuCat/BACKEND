from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Perfil
from spaces.models import Space
from tags.models import Tag

class TestUsers(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        
        self.user = Perfil.objects.create(id=1,username='test_user', is_active=True)
        self.user2 = Perfil.objects.create(id=2,username='test_user2', is_active=True)
        self.space = Space.objects.create(id=1, nom="Bcn", latitud=3.3, longitud=3.3)
        self.space2 = Space.objects.create(id=2, nom="Bdn", latitud=3.2, longitud=3.2)
        self.tag1 = Tag.objects.create(id=1, nom="tag1")
        self.tag2 = Tag.objects.create(id=2, nom="tag2")
        self.user.tags_preferits.set([self.tag1, self.tag2])
        self.user.espais_preferits.set([self.space, self.space2])

    def test_creations_self(self):
        self.assertEqual(Space.objects.count(), 2)
        self.assertEqual(Perfil.objects.count(), 2)
        self.assertEqual(Tag.objects.count(), 2)

    def test_delete_espai_preferit(self):
        response = self.client.delete("/users/1/espais_preferits/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user.espais_preferits.count(), 1)

    def test_delete_tag_preferit(self):
        response = self.client.delete("/users/1/tags_preferits/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user.tags_preferits.count(), 1)