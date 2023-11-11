from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from user.models import Perfil
from events.models import Event
from trophy.models import Trophy
from discount.models import Discount
from .models import Comment
from .views import CommentsView


import string
import random
from user.models import User

#class Test for model Commment
class TestComments(TestCase):
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
        self.comment2 = Comment.objects.create(
            text = 'comentario de prueba 2',
            user = self.user,
            event = self.esdeveniment1
        )
        self.trophy = Trophy.objects.create(
            nom = "Reviwer",
            descripcio = "Quants comentaris has escrit",
            punts_nivell1 = 2,
            punts_nivell2 = 3,
            punts_nivell3 = 5
        )

    #First TestCase, checking everything OK on setUp
    def test_creations_self(self):
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Perfil.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 2)
      
    #POST TestCase  
    def test_post_comment(self):
        data = {
            'text': 'test_comment',
            'event': 1
        }
        CommentsView.apply_permissions = False
        response = self.client.post('/comments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 3)
        CommentsView.apply_permissions = True
        
    #GET by id TestCase
    def test_get_specific_comment(self):
        response = self.client.get(f'/comments/{self.comment2.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['text'], self.comment2.text)
        self.assertEqual(response.data['event'], self.comment2.event.id)
        self.assertEqual(response.data['user'], self.comment2.user.id)
        
    #GET all TestCase
    def test_list_comments(self):
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    #GET comments given an event, checking integration with Event
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
        
    def test_achiveTrophy_getDiscount(self):
        #como user ha hecho dos coments, debe de tener ya un descuento por conseguir nivel1
        
        t_comments = Trophy.objects.get(nom="Reviwer")
        count_check=Comment.objects.filter(user= self.comment1.user).count()
        if count_check == t_comments.punts_nivell1:
            nivell = 1
        elif count_check == t_comments.punts_nivell2:
            nivell = 2
        elif count_check == t_comments.punts_nivell3:
            nivell = 3
        else:
            nivell = None
            
        if nivell is not None:
            caracteres_validos_codigo = string.ascii_uppercase + string.digits
            codigo_descuento= ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
            while Discount.objects.filter(codi=codigo_descuento).exists():
                codigo_descuento = ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
                    
            Discount.objects.create(codi=codigo_descuento,userDiscount=User.objects.get(id=1),nivellTrofeu=nivell,nomTrofeu="Reviwer",usat=False)
        
        self.assertEqual(Discount.objects.count(), 1)
        
        #ahora añado otro para conseguir el 2n descuento
        self.comment4 = Comment.objects.create(
            text = 'comentario de prueba',
            user = self.user,
            event = self.esdeveniment1
        )
        
        t_comments = Trophy.objects.get(nom="Reviwer")
        count_check=Comment.objects.filter(user= self.comment1.user).count()
        if count_check == t_comments.punts_nivell1:
            nivell = 1
        elif count_check == t_comments.punts_nivell2:
            nivell = 2
        elif count_check == t_comments.punts_nivell3:
            nivell = 3
        else:
            nivell = None
            
        if nivell is not None:
            caracteres_validos_codigo = string.ascii_uppercase + string.digits
            codigo_descuento= ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
            while Discount.objects.filter(codi=codigo_descuento).exists():
                codigo_descuento = ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
                    
            Discount.objects.create(codi=codigo_descuento,userDiscount=User.objects.get(id=1),nivellTrofeu=nivell,nomTrofeu="Reviwer",usat=False)
        
        self.assertEqual(Discount.objects.count(), 2)
        
        #ahora añado otro para conseguir el 3r descuento, faltaría uno más
        self.comment5 = Comment.objects.create(
            text = 'comentario de prueba',
            user = self.user,
            event = self.esdeveniment1
        )
        
        t_comments = Trophy.objects.get(nom="Reviwer")
        count_check=Comment.objects.filter(user= self.comment1.user).count()
        if count_check == t_comments.punts_nivell1:
            nivell = 1
        elif count_check == t_comments.punts_nivell2:
            nivell = 2
        elif count_check == t_comments.punts_nivell3:
            nivell = 3
        else:
            nivell = None
            
        if nivell is not None:
            caracteres_validos_codigo = string.ascii_uppercase + string.digits
            codigo_descuento= ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
            while Discount.objects.filter(codi=codigo_descuento).exists():
                codigo_descuento = ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
                    
            Discount.objects.create(codi=codigo_descuento,userDiscount=User.objects.get(id=1),nivellTrofeu=nivell,nomTrofeu="Reviwer",usat=False)
        
        self.assertEqual(Comment.objects.filter(user= self.comment1.user).count(), 4)
        self.assertEqual(Discount.objects.count(), 2)
        #ahora añado otro para conseguir el 3r descuento
        self.comment6 = Comment.objects.create(
            text = 'comentario de prueba',
            user = self.user,
            event = self.esdeveniment1
        )
        
        t_comments = Trophy.objects.get(nom="Reviwer")
        count_check=Comment.objects.filter(user= self.comment1.user).count()
        if count_check == t_comments.punts_nivell1:
            nivell = 1
        elif count_check == t_comments.punts_nivell2:
            nivell = 2
        elif count_check == t_comments.punts_nivell3:
            nivell = 3
        else:
            nivell = None
            
        if nivell is not None:
            caracteres_validos_codigo = string.ascii_uppercase + string.digits
            codigo_descuento= ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
            while Discount.objects.filter(codi=codigo_descuento).exists():
                codigo_descuento = ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
                    
            Discount.objects.create(codi=codigo_descuento,userDiscount=User.objects.get(id=1),nivellTrofeu=nivell,nomTrofeu="Reviwer",usat=False)
        
        self.assertEqual(Discount.objects.count(), 3)
        