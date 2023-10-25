from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from user.models import Perfil
from events.models import Event
from .models import Comment
from .views import CommentsView


class TestCommentsPost(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        
        self.user = Perfil.objects.create(id=1,username='test_user', is_active=True)
        self.esdeveniment1 = Event.objects.create(id=1, nom="test_event1")
        self.esdeveniment2 = Event.objects.create(id=2, nom="test_event2")
        self.comment1 = Comment.objects.create(
            text = 'comentario de prueba',
            user = self.user,
            event = self.esdeveniment1
        )

    def test_creations_self(self):
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Perfil.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)
        
    def test_post_comment(self):
        data = {
            'text': 'test_comment',
            'event': 1
        }
        CommentsView.apply_permissions = False
        response = self.client.post('/comments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        CommentsView.apply_permissions = True
        
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
        event_id = 1
        self.comment2 = Comment.objects.create(
            text = 'comentario de prueba 2',
            user = self.user,
            event = self.esdeveniment1
        )
        self.comment3 = Comment.objects.create( #comentario asociado a otro evento diferente
            text = 'comentario de prueba 3',
            user = self.user,
            event = self.esdeveniment2
        )
        response = self.client.get(f'/comments/?event={event_id}')

        self.assertEqual(response.status_code, 200)
        comments = response.data['results']
        self.assertTrue(comments)

        comment_in_response = next((comment for comment in comments if comment['event'] == event_id), None)
        self.assertIsNotNone(comment_in_response) 