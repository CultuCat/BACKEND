from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from discount.models import Discount
from user.models import Perfil
from django.urls import reverse

class TestDiscounts(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        
        self.user = Perfil.objects.create(id=1,username='test_user', is_active=True)
        self.discount1 = Discount.objects.create(
            codi = "AAAAAA",
            userDiscount = self.user,
            nivellTrofeu = 2,
            nomTrofeu = "Reviewer",
            usat = False
        )
        
    def test_creations_self(self):
        self.assertEqual(Discount.objects.count(), 1)
        
    def test_get_discounts_byUser(self):
        query_params = {'user': '1'}

        response = self.client.get('/discounts/', query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['codi'], "AAAAAA")
        
        self.discount2 = Discount.objects.create(
            codi = "BBBBBB",
            userDiscount = self.user,
            nivellTrofeu = 1,
            nomTrofeu = "Reviewer",
            usat = False
        )
        
        self.discount3 = Discount.objects.create(
            codi = "CCCCCC",
            userDiscount = self.user,
            nivellTrofeu = 3,
            nomTrofeu = "Reviewer",
            usat = True
        )
        
        response = self.client.get('/discounts/', query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        #el orden es ascendente según nombre de trofeo, nivelTrofeo, los usados no se listan
        self.assertEqual(response.data[0]['codi'], "BBBBBB")
        self.assertEqual(response.data[1]['codi'], "AAAAAA")
        
    # def test_get_discount_fals_INVALID(self):
    #     url = reverse('verificar_descuento') 
    #     query_params = {'discount': 'AAAAAAA'}

    #     response = self.client.get(url, query_params)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertFalse(response.data['existe_descuento'])
        
    # def test_get_discount_usat_INVALID(self):
    #     self.discount2 = Discount.objects.create(
    #         codi = "AS12WE35",
    #         userDiscount = self.user,
    #         nivellTrofeu = 3,
    #         nomTrofeu = "Reviewer",
    #         usat = True
    #     )
    #     url = reverse('verificar_descuento')  
    #     query_params = {'discount': 'AS12WE35'}

    #     response = self.client.get(url, query_params)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertFalse(response.data['existe_descuento'])
        
    # def test_get_discount_altreUser_INVALID(self):
    #     self.user2 = Perfil.objects.create(id=2,username='test_user2', is_active=True)
    #     self.discount2 = Discount.objects.create(
    #         codi = "AS12WE35",
    #         userDiscount = self.user2,
    #         nivellTrofeu = 3,
    #         nomTrofeu = "Reviewer",
    #         usat = True
    #     )
    #     url = reverse('verificar_descuento')
    #     query_params = {'discount': 'AS12WE35'}

    #     response = self.client.get(url, query_params)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertFalse(response.data['existe_descuento'])
    
   