from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from user.models import Perfil
from ticket.models import Ticket
from . import permissions
from user.views import PerfilView



class PerfilViewTests(TestCase):
    def setUp(self):
        self.user = Perfil.objects.create(username='testuser', email='testuser@example.com', is_active=True)
        self.user.set_password('testpassword')
        self.user.save()
        self.admin = Perfil.objects.create(username='testadmin', email='testadmin@example.com', is_active=True, isAdmin=True)

        self.token = Token.objects.create(user=self.user)


    #test qualsevol usuari autenticat
    def test_authenticated_true(self):
        request = APIRequestFactory().get('')
        request.user = self.user
        permission = permissions.IsAuthenticated()
        self.assertTrue(permission.has_permission(request))

    #test no usuari, no autentificat
    def test_authenticated_false(self):
        request = APIRequestFactory().get('')
        request.user = None
        permission = permissions.IsAuthenticated()
        self.assertFalse(permission.has_permission(request))

    #Comprova si ets administrador
    def test_admin_true(self):
        request = APIRequestFactory().get('')
        request.user = self.admin
        permission = permissions.IsAdmin()
        self.assertTrue(permission.has_permission(request))

    #Comprova si no ets administrador
    def test_admin_false(self):
        request = APIRequestFactory().get('')
        request.user = self.user
        permission = permissions.IsAdmin()
        self.assertFalse(permission.has_permission(request))

    #update amb usuari no autenticat
    def test_profile_update_unauthenticated(self):
        url = f'/users/{self.user.id}/'
        data = {'imatge': 'newimage.jpg', 'bio': 'New bio'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_user(self):
        #Crear usuari correctament
        data = {
            'username': 'nuevo_usuario',
            'email': 'nuevo_usuario@example.com',
            'password': 'contrasena123'
        }
        PerfilView.apply_permissions = False
        response = self.client.post('/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        PerfilView.apply_permissions = True

        # Intentar crear un usuari amb el mateix nom d'usuari (error)
        data_duplicada = {
            'username': 'nuevo_usuario',
            'email': 'otro_usuario@example.com',
            'password': 'otra_contrasena456',
        }
        PerfilView.apply_permissions = False
        response = self.client.post('/users/', data_duplicada, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        PerfilView.apply_permissions = True


    def test_get_specific_user(self):
        #hacemos get de user1
        response = self.client.get(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_list_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


"""
    #update correcte amb usuari autenticat
    def test_profile_update(self):
        data = {'imatge': 'newimage.jpg', 'bio': 'New bio'}
        response = self.client.put(f'/users/{self.user.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.perfil.imatge, 'newimage.jpg')
        self.assertEqual(self.user.perfil.bio, 'New bio')    
"""

"""
class TicketUsersViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Perfil.objects.create(username='testuser')
        self.ticket = Ticket.objects.create(user=self.user, event=1)

    def test_get_event_users(self):
        event_id = 5 
        url = f'/users/tickets/{event_id}/users/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
"""
