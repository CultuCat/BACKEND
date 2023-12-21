from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from user.models import Perfil
from trophy.models import Trophy
from .models import Message
from .views import MessageAPIView
from rest_framework.authtoken.models import Token

#class Test for model Message
class TestMessages(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        
        self.user1 = Perfil.objects.create(id=1, username='test_user1', is_active=True)
        self.user2 = Perfil.objects.create(id=2, username='test_user2', is_active=True)
        self.user3 = Perfil.objects.create(id=3, username='test_user3', is_active=True)
        self.token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.message1 = Message.objects.create(user_to=self.user1, user_from=self.user2, text="holi1")
        self.message2 = Message.objects.create(user_to=self.user2, user_from=self.user1, text="holi2")
        self.trophy = Trophy.objects.create(
            nom = "Xerraire",
            descripcio = "Quants missatges has escrit",
            punts_nivell1 = 1,
            punts_nivell2 = 2,
            punts_nivell3 = 3
        )
        self.trophy2 = Trophy.objects.create(
            nom = "Col·leccionista d'or",
            descripcio = "Quants trofeus d'or",
            punts_nivell1 = 1,
            punts_nivell2 = 2,
            punts_nivell3 = 3
        )

    #First TestCase, checking everything OK on setUp
    def test_creations_self(self):
        self.assertEqual(Perfil.objects.count(), 3)
        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(Trophy.objects.count(), 2)
    
    #POST TestCase  
    def test_post_message(self):
        data = {
            'user_to': 1, 
            'user_from': 2, 
            'text': "qtal1"
        }
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}
        response = self.client.post('/messages/', data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 3)
        
        data = {
            'user_to': 1, 
            'user_from': 2, 
            'text': "tasbien1?"
        }
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}
        response = self.client.post('/messages/', data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 4)
        
    #GET all given 2 users
    def test_list_messages(self):
        #obtenemos los 2 mensajes del inicio
        response = self.client.get('/messages/?user1=1&user2=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        
        #creamos 2 mensajes nuevos, 1 de la conversación previa y otro que no
        data = {
            'user_to': 1, 
            'user_from': 2, 
            'text': "qtal1"
        }
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}
        response = self.client.post('/messages/', data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'user_to': 3, 
            'user_from': 2, 
            'text': "qtal1"
        }
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}
        response = self.client.post('/messages/', data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        #ahora se obtienen 3 mensajes
        response = self.client.get('/messages/?user1=1&user2=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)