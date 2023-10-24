from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from user.models import User, Perfil
from events.models import Event
from .models import Comment


class TestCommentsPost(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        
        self.user = User.objects.create(id=1,username='test_user', is_active=True)
        self.perfil = Perfil.objects.create(user=self.user)
        self.esdeveniment1 = Event.objects.create(id=1, nom="test_event1")
        self.esdeveniment2 = Event.objects.create(id=2, nom="test_event2")
        self.comment1 = Comment.objects.create(
            text = 'comentario de prueba',
            user = self.user,
            event = self.esdeveniment1
        )

    def test_creations_self(self):
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Perfil.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        
    def test_post_comment(self):
        data = {
            'text': 'test_comment',
            'event': 1
        }
        response = self.client.post('/comments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        
    def test_get_specific_event(self):
        response = self.client.get(f'/comments/{self.comment1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['text'], self.comment1.text)
        self.assertEqual(response.data['event'], self.comment1.event.id)
        self.assertEqual(response.data['user'], self.comment1.user.id)
        
    def test_list_comments(self):
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_list_comments_by_event(self):
        self.comment2 = Comment.objects.create(
            text = 'comentario de prueba 2',
            user = self.user,
            event = self.esdeveniment1
        )
        event_id = 1
        response = self.client.get(f'/comments/?event={event_id}')

        self.assertEqual(response.status_code, 200)
        comments = response.data['results']
        self.assertTrue(comments)

        comment_in_response = next((comment for comment in comments if comment['event'] == event_id), None)
        self.assertIsNotNone(comment_in_response) 