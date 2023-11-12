from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from user.models import Perfil
from events.models import Event
from discount.models import Discount
from trophy.models import Trophy
from .models import Ticket
from .views import TicketsView

import string
import random
from user.models import User


class TestTicketsPost(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        
        self.user = Perfil.objects.create(id=1,username='test_user', is_active=True)
        self.user2 = Perfil.objects.create(id=2,username='test_user2', is_active=True)
        self.esdeveniment1 = Event.objects.create(id=1, nom="test_event1")
        self.esdeveniment2 = Event.objects.create(id=2, nom="test_event2")
        #creamos ticket para user 1 en evento 2
        self.ticket1 = Ticket.objects.create(
            user = self.user,
            event = self.esdeveniment2
        )
        
        #creamos ticket para user 2 en evento 2
        self.ticket2 = Ticket.objects.create(
            user = self.user2,
            event = self.esdeveniment2
        )
        
        self.trophy = Trophy.objects.create(
            nom = "Més esdeveniments",
            descripcio = "Quants esdeveniments has assist",
            punts_nivell1 = 2,
            punts_nivell2 = 3,
            punts_nivell3 = 5
        )

    def test_creations_self(self):
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Perfil.objects.count(), 2)
        self.assertEqual(Ticket.objects.count(), 2)
        self.assertEqual(Trophy.objects.count(), 1)
        
    def test_post_ticket(self):
        #creamos un ticket para el user 1 en evento 1, deja crear
        data = {
            'event': 1
        }
        TicketsView.apply_permissions = False
        response = self.client.post('/tickets/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 3)
        TicketsView.apply_permissions = True
        
        #creamos un ticket para el user 1 en evento 1, no deja crear, ya existe
        data = {
            'event': 2
        }
        TicketsView.apply_permissions = False
        response = self.client.post('/tickets/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Ticket.objects.count(), 3)
        TicketsView.apply_permissions = True
        
    def test_get_specific_ticket(self):
        #hacemos get de ticket1
        response = self.client.get(f'/tickets/?event={self.ticket1.event.id}&user={self.ticket1.user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['event'], self.ticket1.event.id) #2 2
        self.assertEqual(response.data[0]['user'], self.ticket1.user.id) #1 2
        
        #hacemos get de ticket2
        response = self.client.get(f'/tickets/?event={self.ticket2.event.id}&user={self.ticket2.user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['event'], self.ticket2.event.id)
        self.assertEqual(response.data[0]['user'], self.ticket2.user.id)
        
    def test_list_tickets(self):
        response = self.client.get('/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
   
    def test_achiveTrophy_getDiscount(self):
        #como ahora el user1 solo tiene un ticket no tiene ningún trofeo/descuento
        self.check_new_trophy()
        self.assertEqual(Discount.objects.count(), 0)
        
        self.esdeveniment3 = Event.objects.create(id=3, nom="test_event3")
        self.ticket3 = Ticket.objects.create(
            user = self.user,
            event = self.esdeveniment3
        )
        
        #ahora al haver 2 tickets sí que ha ganado un trofeo/descuento
        self.check_new_trophy()
        self.assertEqual(Discount.objects.count(), 1)
        
        #ahora añado otro para conseguir el 2n descuento
        self.esdeveniment4 = Event.objects.create(id=4, nom="test_event4")
        self.ticket4 = Ticket.objects.create(
            user = self.user,
            event = self.esdeveniment4
        )
        self.check_new_trophy()
        self.assertEqual(Discount.objects.count(), 2)
        
        #ahora añado otro, pero no llega para el nivel3 del trofeo
        self.esdeveniment5 = Event.objects.create(id=5, nom="test_event5")
        self.ticket5 = Ticket.objects.create(
            user = self.user,
            event = self.esdeveniment5
        )
        self.check_new_trophy()
        self.assertEqual(Discount.objects.count(), 2) #como no se ha ganado nada sigue habiendo 2
        
        #añado otro, ahora se consigue el nivel 3
        self.esdeveniment6 = Event.objects.create(id=6, nom="test_event6")
        self.ticket6 = Ticket.objects.create(
            user = self.user,
            event = self.esdeveniment6
        )
        self.check_new_trophy()
        self.assertEqual(Discount.objects.count(), 3) #nivel3 conseguido
        
        
    def check_new_trophy(self):
        t_tickets = Trophy.objects.get(nom="Més esdeveniments")
        count_check= Ticket.objects.filter(user= self.ticket1.user).count()
        if count_check == t_tickets.punts_nivell1:
            nivell = 1
        elif count_check == t_tickets.punts_nivell2:
            nivell = 2
        elif count_check == t_tickets.punts_nivell3:
            nivell = 3
        else:
            nivell = None
            
        if nivell is not None:
            caracteres_validos_codigo = string.ascii_uppercase + string.digits
            codigo_descuento= ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
            while Discount.objects.filter(codi=codigo_descuento).exists():
                codigo_descuento = ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
                    
            Discount.objects.create(codi=codigo_descuento,userDiscount=User.objects.get(id=1),nivellTrofeu=nivell,nomTrofeu="Més esdeveniments",usat=False)
        
    
    def test_disable_discount(self):
        #conseguimos un trofeo:
        self.esdeveniment3 = Event.objects.create(id=3, nom="test_event3")
        self.ticket3 = Ticket.objects.create(
            user = self.user,
            event = self.esdeveniment3
        )
        self.check_new_trophy()
        self.assertEqual(Discount.objects.count(), 1)
        
        #usamos el descuento, y comprobamos q pasa el bool usat de False->True:
        descuentos = Discount.objects.all()
        self.assertEqual(descuentos[0].usat, False)
        self.esdeveniment4 = Event.objects.create(id=4, nom="test_event4")
        data = {
            'event': 4,
            'discount' : descuentos[0].codi
        }
        TicketsView.apply_permissions = False
        response = self.client.post('/tickets/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 4)
        self.assertEqual(descuentos[0].usat, True)
        TicketsView.apply_permissions = True
    
    