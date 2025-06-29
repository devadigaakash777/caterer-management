from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from . import setup_test_data

from caterer.forms import CreateUserForm,FoodForm,MenuCategoryItemForm,MenuCategoryForm,CateringServiceForm,CateringBranchForm,CateringPackageForm,AddressForm,PhoneContactForm
from catrinmodel.models import CateringService, CateringBranch, Food, CatererFood, MenuCategoryDetails, Address, Order, OrderedFood, Delivery, MenuCategory
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import force_authenticate, APIRequestFactory
#from catrinmodel.urls import reverse
from decimal import Decimal

from . import setup_test_data
from catrinmodel.views import *  # Adjust the import path accordingly
from caterer.CatererMethods import Location  # Assuming you have a Location helper with haversine()


class CheckNearbyCaterersViewTest(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.test_data = setup_test_data()  # Load test data
        self.user3=self.test_data["caterersList"][0]
        self.user1 = self.test_data["usersList"][0]
        self.branch1 = self.test_data["branchesList"][0]
        
    @patch('caterer.views.Location.haversine')
    def test_check_view(self, mock_haversine):
        mock_haversine.return_value = Decimal('5.0')
        self.client.login(username=self.user1.username, password="password123")
        session=self.client.session
        user = self.user1 
        user_address=user.addresses.filter(is_active=True).first()
        session['userlongitude'] = float(user_address.longitude)
        session['userlatitude'] = float(user_address.latitude)
        
        session.save()  
        response = self.client.get(reverse('catrinmodel:api-check'))

        # all_caterers = response.context['all_caterers']
        # caterers_names = [caterer.branch_id.caterer_name for caterer in all_caterers]

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.context['isCaterer'], False)
        # self.assertEqual(len(response.context['all_caterers']),2)
        # self.assertEqual(response.context['user'], self.user1)
        # self.assertIn('Caterer One',caterers_names)
        
    @patch('caterer.views.Location.haversine')
    def test_check_caterer_view(self, mock_haversine):
        mock_haversine.return_value = Decimal('5.0')
        self.client.login(username="user3", password="password123")
        session=self.client.session
        user = self.user3 
        user_address=user.addresses.filter(is_active=True).first()
        session['userlongitude'] = float(user_address.longitude)
        session['userlatitude'] = float(user_address.latitude)
        
        session.save()  
        response = self.client.get(reverse('catrinmodel:api-check'))
        # all_caterers = response.context['all_caterers']
        # usernames = [caterer.branch_id.caterer_id.username for caterer in all_caterers]

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.context['isCaterer'], True)
        # self.assertEqual(len(response.context['all_caterers']),2)
        # self.assertEqual(response.context['user'], self.user3)
        # self.assertIn('user3',usernames)


import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from catrinmodel.models import Order


class CateringAppTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Initialize all test data safely from test_utils.py
        cls.data = setup_test_data()
        cls.user1 = cls.data['usersList'][0]
        cls.user2 = cls.data['usersList'][1]
        cls.order = cls.data['ordersList'][0]

    def setUp(self):
        # Login user1 for tests requiring authentication
        self.client.login(username='user1', password='password123')

    def test_my_view_post_valid(self):
        url = reverse('my_view')
        payload = {'key1': '12.9141', 'key2': '74.8560'}
        response = self.client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {'message': 'Data received', 'received_data': payload}
        )
        # Verify session variables set correctly
        session = self.client.session
        self.assertEqual(session.get('userlatitude'), '12.9141')
        self.assertEqual(session.get('userlongitude'), '74.8560')

    def test_my_view_get_not_allowed(self):
        url = reverse('my_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Only POST requests are allowed'})

    def test_check_view_renders_for_authenticated(self):
        url = reverse('home')
        # Setup session with necessary keys to prevent error
        session = self.client.session
        session['userlatitude'] = '12.9141'
        session['userlongitude'] = '74.8560'
        session.save()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'check.html')
        self.assertIn('isCaterer', response.context)
        self.assertIn('all_caterers', response.context)

    def test_check_view_error_handling_missing_session(self):
        url = reverse('home')
        # Not setting required session keys to test error handling
        response = self.client.get(url)
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Error:', response.content)

    def test_register_page_get(self):
        url = reverse('register')
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_page_post_invalid_data(self):
        url = reverse('register')
        self.client.logout()
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please fix the errors below.")

    def test_login_page_get(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_redirects_login(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login'))

    def test_order_view_get_and_post(self):
        url = reverse('order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order.html')

        post_data = {
            "orderDate": "2024-06-01",
            "orderTime": "18:00",
            "functionName": "Test Function",
            "functionNonMember": "3",
            "functionVegMember": "5",
            "zip": "575001"
        }
        response_post = self.client.post(url, data=post_data)
        self.assertEqual(response_post.status_code, 302)  # Redirect to menu view
        self.assertEqual(self.client.session['functionVegMember'], "5")
        self.assertEqual(self.client.session['functionName'], "Test Function")
        self.assertEqual(self.client.session['userZipCode'], "575001")

    def test_delivery_view_get_and_post(self):
        # Setup session variables needed
        session = self.client.session
        user1 = self.data['usersList'][0]
        user_address=user1.addresses.filter(is_active=True).first()
        
        session['userZipCode'] = user_address.zip_code
        session['functionName'] = 'Wedding'
        session['functionNonMember'] = 50
        session['functionVegMember'] = 25
        session['branch_id'] = str(self.data['branchesList'][0].id)
        session['selected_items'] = [str(food.pk) for food in self.data['caterer_foodsList']]
        session['userlatitude'] = '12.9141'
        session['userlongitude'] = '74.8560'
        session.save()

        url = reverse('delivery')

        # GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delivery.html')
        self.assertIn('totalAmount', response.context)

        # POST request with payment amount and note
        post_data = {'amount': '250.00', 'note': 'Payment note'}
        response_post = self.client.post(url, data=post_data)
        self.assertIn(response_post.status_code, [302, 200])  # Redirect success or error render

    def test_remove_view_get(self):
        url = reverse('remove')
        session = self.client.session
        session['selected_items'] = ['1', '2', '3']
        session.save()
        response = self.client.get(f"{url}?delete=2")
        self.assertEqual(response.status_code, 302)  # Redirect after removal
        self.assertNotIn('2', self.client.session.get('selected_items', []))

    def test_full_order_details_view(self):
        url = reverse('FullOrderDetails', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'FullOrderDetails.html')
        self.assertIn('selected_items', response.context)
        self.assertIn('type', response.context)


