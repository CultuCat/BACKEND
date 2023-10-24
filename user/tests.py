from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token
from user.models import Perfil
from ticket.models import Ticket
from . import permissions

class PerfilViewTests(TestCase):
    def setUp(self):
        self.user = Perfil.objects.create(id='1', username='testuser', email='testuser@example.com', is_active=True)
        self.user.set_password('testpassword')
        self.user.save()
        self.admin = Perfil.objects.create(id='2', username='testadmin', email='testadmin@example.com', is_active=True, isAdmin=True)


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
"""
    def test_profile_update(self):
        url = '/users/perfils/1/profile'
        data = {'password': 'newpassword', 'imatge': 'newimage.jpg', 'bio': 'New bio'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.check_password('newpassword'), True)
        self.assertEqual(self.user.perfil.imatge, 'newimage.jpg')
        self.assertEqual(self.user.perfil.bio, 'New bio')

class SignInGoogleViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_sign_in_google(self):
        url = reverse('sign-in-google', args=['google'])
        data = {'access_token': 'your-access-token'}  # Replace with a valid access token
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TicketUsersViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Perfil.objects.create(username='testuser')
        self.ticket = Ticket.objects.create(user=self.user, event=1)

    def test_get_ticket_users(self):
        ticket_id = 5  # Replace with the actual ticket ID
        url = f'/users/tickets/{ticket_id}/users/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

"""