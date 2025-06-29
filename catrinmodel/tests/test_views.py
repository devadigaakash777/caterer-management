from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch  #MagicMock,
from catrinmodel.models import CateringService, CateringBranch, Address, CateringPackage
from caterer.views import check,menu
from django.contrib.auth.models import User
from catrinmodel.models import *
from decimal import Decimal
from caterer.CatererMethods import *
from datetime import date, time
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from . import setup_test_data



class CheckViewTestCase(TestCase):
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
        response = self.client.get(reverse('home'))
        
        all_caterers = response.context['all_caterers']
        caterers_names = [caterer.branch_id.caterer_name for caterer in all_caterers]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['isCaterer'], False)
        self.assertEqual(len(response.context['all_caterers']),2)
        self.assertEqual(response.context['user'], self.user1)
        self.assertIn('Caterer One',caterers_names)
        
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
        response = self.client.get(reverse('home'))
        all_caterers = response.context['all_caterers']
        usernames = [caterer.branch_id.caterer_id.username for caterer in all_caterers]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['isCaterer'], True)
        self.assertEqual(len(response.context['all_caterers']),2)
        self.assertEqual(response.context['user'], self.user3)
        self.assertIn('user3',usernames)

    
        #self.assertIn("Caterer Two", response.content.decode())
        
class MenuTestCase(TestCase):
    def setUp(self):
        # Set up test data
        self.test_data = setup_test_data()  # Load test data
        # self.user3 = self.test_data["caterersList"][0]
        self.user1 = self.test_data["usersList"][0]
        self.branch1 = self.test_data["branchesList"][0]

    def test_user_can_see_menu(self):
        # Test that the user can access the menu and see selected items
        self.client.login(username="user1", password="password123")
        session = self.client.session
        session['branch_id'] = self.branch1.pk
        session.save()

        response = self.client.get(reverse('menu'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(session.get('branch_id'), int)
        self.assertEqual(len(response.context['record']), 3)

    def test_user_adds_items_to_menu(self):
        # Test that the user can add items to the menu
        self.client.login(username="user1", password="password123")
        session = self.client.session
        session['branch_id'] = self.branch1.pk
        selected_items = self.branch1.caterer_food_details.last().pk
        session['selected_items'] = [selected_items]
        session.save()

        response = self.client.post(reverse('menu'), {
            'add_item': 'add', 
            'items': [str(item.pk) for item in self.branch1.caterer_food_details.all()]
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['selected_items']), 3)
        self.assertEqual(len(response.context['record']), 0)
        food_names = [item.food.name for item in response.context['selected_items']]
        self.assertIn("Pasta", food_names)

    def test_user_submits_order(self):
        # Test that the user can submit the order and is redirected
        self.client.login(username="user1", password="password123")
        session = self.client.session
        session['branch_id'] = self.branch1.pk
        selected_items = self.branch1.caterer_food_details.last().pk
        session['selected_items'] = [selected_items]
        session.save()

        response = self.client.post(reverse('menu'), {
            'add_to_order': 'submit', 
        })
        
        # self.assertEqual(response.status_code, 302)
        # expected_url = response['Location']
        # self.assertTrue(expected_url.startswith(reverse('delivery')))
        
        
    def test_error_in_menu(self):
        session = self.client.session
        session['branch_id'] = self.branch1.pk
        session.save()
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/menu/')
        
        self.client.login(username="user1", password="password123")
        session = self.client.session
        session['branch_id'] = 9
        session.save()
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 404)


class OrderTestCase(TestCase):
    def setUp(self):
        # Set up test data
        self.test_data = setup_test_data()  # Load test data
        self.user1 = self.test_data["usersList"][0]
        self.branch1 = self.test_data["branchesList"][0]
        self.client.login(username="user1", password="password123")
    def test_order_get_method(self):
        # Simulate a GET request
        
        response = self.client.get(reverse('order'), {'branch': self.branch1.pk})
        
        # Check that the session has been set correctly
        session = self.client.session

        self.assertEqual(session['branch_id'], str(self.branch1.pk))
        
        # Check the status code is OK (200)
        self.assertEqual(response.status_code, 200)
    
    def test_order_post_method(self):
        # Simulate a POST request
        response = self.client.get(reverse('order'), {'branch': self.branch1.pk})
        response = self.client.post(reverse('order'), {
            'orderDate': '2025-01-01',
            'orderTime': '12:00',
            'functionName': 'Wedding',
            'functionNonMember': '50',
            'functionVegMember': '25',
            'zip': '12345'
        })
        
        # Check that the session data is set correctly
        session = self.client.session
        self.assertEqual(session['branch_id'], str(self.branch1.pk))
        self.assertEqual(session.get('orderDate'), '2025-01-01')
        self.assertEqual(session.get('orderTime'), '12:00')
        self.assertEqual(session.get('functionName'), 'Wedding')
        self.assertEqual(session.get('functionNonMember'), '50')
        self.assertEqual(session.get('functionVegMember'), '25')
        self.assertEqual(session.get('userZipCode'), '12345')
        
        # Check the redirection status
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('menu'))

class DeliveryTestCase(TestCase):
    def setUp(self):
        # Set up test data
        self.test_data = setup_test_data()  # Load test data
        self.user1 = self.test_data["usersList"][1]
        self.branch1 = self.test_data["branchesList"][0]
        user_address=self.user1.addresses.filter(is_active=True).first()
        self.session = self.client.session
        self.session['branch_id'] = self.branch1.pk
        # selected_items = self.branch1.caterer_food_details.all().pk
        # self.session['selected_items'] = [selected_items]
        selected_items = self.branch1.caterer_food_details.values_list('pk', flat=True)
        self.session['selected_items'] = list(selected_items)
        self.session['userZipCode'] = user_address.zip_code
        self.session['functionName'] = 'Wedding'
        self.session['functionNonMember'] = 50
        self.session['functionVegMember'] = 25
        
        
        self.session['userlongitude'] = float(user_address.longitude)
        self.session['userlatitude'] = float(user_address.latitude)
        self.session.save()
        
        #login as user1
        #self.client.login(username="user1", password="password123")
    
    def test_delivery_get_method(self):
        self.client.login(username="user2", password="password123")
        response = self.client.get(reverse('delivery'))

        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the session data was loaded correctly
        session = self.client.session
        self.assertEqual(session.get('branch_id'), self.branch1.pk)
        self.assertIn('selected_items', response.context)
        self.assertIn('delivery_cost', response.context)
        self.assertIn('totalAmountFood', response.context)
        self.assertIn('totalAmount', response.context)
        self.assertIn('advanceAmount', response.context)
        # self.assertEqual(response.context['totalAmountFood'],7750)
        # self.assertEqual(response.context['delivery_cost'],2200)
        
        '''Delivery cost is equal to haversine distnce between user(long,lat) and caterer(long,lat) as total_distance
            total_distance_except_free_delivery_distance = total_distance - free_delivery_distance
            total_delivery_cost = total_distance_except_free_delivery_distance * delivery_cost_per_km
        '''
        
    def test_delivery_locate_address_method(self):
        self.client.login(username="user4", password="password123")
        response = self.client.get(reverse('delivery'))

    
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/create-address-phone/?entity_type=user')
        
    def test_delivery_post_method(self):
        self.client.login(username="user2", password="password123")
        response = self.client.post(reverse('delivery'), {
            'amount': '8850',
            'note': 'Extra plates required',
        })

        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, 302)
        orders = self.user1.user_orders.last()
        delivery=orders.delivery_details
        ordered_foods=orders.food_items.all()
        # Loop through each instance and print its fields and values
        #for order in orders:
            
        # print(f"--- ORDER ID: {orders.id} ---")
        # for field, value in orders.__dict__.items():
        #     if not field.startswith('_'):  # Skip internal Django attributes like '_state'
        #         print(f"{field}: {value}")
            
        # print(f"--- DELIVERY ID: {delivery.id} ---")
        # for field, value in delivery.__dict__.items():
        #     if not field.startswith('_'):  # Skip internal Django attributes like '_state'
        #         print(f"{field}: {value}")

        # for ordered_food in ordered_foods:
        #     print(f"--- ordered_food ID: {ordered_food.id} ---")
        #     for field, value in ordered_food.__dict__.items():
        #         if not field.startswith('_'):  # Skip internal Django attributes like '_state'
        #             print(f"{field}: {value}")
        #     print()  # Add a blank line between addresses
            
        self.assertEqual(orders.user, self.user1)
        self.assertEqual(delivery.order, orders)
        self.assertEqual(len(ordered_foods), len(self.session['selected_items']))
                
                


