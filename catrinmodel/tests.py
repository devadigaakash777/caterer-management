# from django.test import TestCase,Client
# from django.urls import reverse 
# from django.shortcuts import render, get_object_or_404
# #from caterer.CatererMethods import Location,Cat_Email,Cat_Bill
# from catrinmodel.models import CateringService, CateringBranch, Food, CatererFood, MenuCategoryDetails, Address, Order, OrderedFood,CancelledOrder,Delivery
# from django.contrib.auth.models import User
# from datetime import datetime
# import decimal
# from django.contrib.auth import get_user_model
# from .models import CateringService, CateringBranch, CateringPackage, Address, Food, BankDetails, Order,PhoneContact
# from django.db.utils import IntegrityError
# from django.core.exceptions import ValidationError
# import datetime
# from django_countries.fields import Country
# from decimal import Decimal
# from phonenumber_field.phonenumber import PhoneNumber
# # Create your tests here.

# class CateringModelTests(TestCase):
    
#     def setUp(self):
#         # Set up test data for User, CateringService, and CateringBranch
#         self.user = User.objects.create_user(username="testuser", password="password")
        
#         Address.objects.create(
#                 entity_type="user",
#                 user=self.user,
#                 street="Another Street",
#                 city="Another City",
#                 zip_code="54321",
#                 state="Another State",
#                 country="IN",
#                 latitude="20.0760",
#                 longitude="73.8777"
#             )
        
#         self.catering_service = CateringService.objects.create(
#             caterer_name="Test Catering",
#             description="Test Description",
#             gstin_number="27AAAPL1234C1Z5",
#             caterer_id=self.user,
#             image="image.jpg"
#         )
#         self.catering_branch = CateringBranch.objects.create(
#             branch_id=self.catering_service,
#             branch_name="Test Branch"
#         )
#         self.catering_package = CateringPackage.objects.create(
#             branch=self.catering_branch,
#             starting_price=1000.00,
#             deliverable_area=10.0,
#             delivery_charge=100.00,
#             free_delivery_till_km=5.0,
#             gst_for_food=5.0,
#             max_order_night=10,
#             max_order_day=20,
#             type="veg",
#             advance_percentage=20.0
#         )
           
#         Address.objects.create(
#                 entity_type="caterer",
#                 branch=self.catering_branch,
#                 street="Another Street",
#                 city="Another City",
#                 zip_code="54321",
#                 state="Another State",
#                 country="IN",
#                 latitude="20.0760",
#                 longitude="73.8777"
#             )
               
#         self.food = Food.objects.create(
#             name="Test Food",
#             type_food="veg",
#             menu_catagory="veg_starter",
#             food_image="some_food.jpeg"
#         )

#         self.food1 = Food.objects.create(name="Veg Soup", type_food="veg", menu_catagory="veg_starter",food_image="some_food.jpeg")
#         self.food2 = Food.objects.create(name="Chicken Curry", type_food="non-veg", menu_catagory="nonveg_main",food_image="some_food.jpeg")
#         self.food3 = Food.objects.create(name="Fruit Juice", type_food="both", menu_catagory="juice",food_image="some_food.jpeg")
            
#     def test_catering_service_creation(self):
#         self.assertEqual(self.catering_service.caterer_name, "Test Catering")
#         self.assertEqual(self.catering_service.gstin_number, "27AAAPL1234C1Z5")
#         self.assertEqual(self.catering_branch.branch_id.caterer_id.username,"testuser")
#         self.assertEqual(self.catering_service.caterer_id, self.user)

#     def test_catering_branch_creation(self):
#         self.assertEqual(self.catering_branch.branch_name, "Test Branch")
#         self.assertEqual(self.catering_branch.branch_id, self.catering_service)

#     def test_catering_package_creation(self):
#         self.assertEqual(self.catering_package.starting_price, 1000.00)
#         self.assertEqual(self.catering_package.deliverable_area, 10.0)
#         self.assertEqual(self.catering_package.type, "veg")

#     def test_food_creation(self):
#         self.assertEqual(self.food.name, "Test Food")
#         self.assertEqual(self.food.type_food, "veg")
#         self.assertEqual(self.food.menu_catagory, "veg_starter")
    
#     def test_multiple_address_for_user(self):
#             address1=Address.objects.create(
#                 entity_type="user",
#                 user=self.user,
#                 street="Another Street",
#                 city="Another City",
#                 zip_code="54321",
#                 state="Another State",
#                 country="IN",
#                 latitude="20.0760",
#                 longitude="73.8777"
#             )
            
#             self.assertEqual(address1.is_active, True)
            
#             address2=Address.objects.create(         
#                 entity_type="user",
#                 user=self.user,
#                 street="Another Street",
#                 city="Another City",
#                 zip_code="54321",
#                 state="Another State",
#                 country="IN",
#                 latitude="-89.763743",
#                 longitude="179.834756"
#             )
#             address1.refresh_from_db()
#             self.assertEqual(address2.longitude,Decimal('179.834756'))
#             self.assertEqual(address1.is_active,False)
#             self.assertEqual(address2.is_active,True)
            
#     def test_address_str_representation(self):
#         address = Address(
#             street="789 Test Blvd",
#             city="Test Town",
#             state="Test Region",
#             country=Country("IN"),
#             zip_code = "578 109"
#         )
#         self.assertEqual(str(address), "789 Test Blvd, Test Town, Test Region, IN, 578 109")       
    
    
#     def test_bank_details_creation_for_caterer(self):
#         bank_detail = BankDetails.objects.create(
#             bank_name="Test Bank",
#             account_holder="Test Holder",
#             account_no="1234567890",
#             ifsc_code="ABCD0123456",
#             bank_type="savings",
#             bank_branch="Test Branch",
#             entity_type="caterer",
#             branch=self.catering_branch
#         )
#         self.assertEqual(bank_detail.bank_name, "Test Bank")
#         self.assertEqual(bank_detail.account_holder, "Test Holder")
#         self.assertEqual(bank_detail.account_no, "1234567890")
        
    
        
#     def test_multiple_bank_for_user(self):
#             bank_detail1 = BankDetails.objects.create(
#                 bank_name="Test Bank",
#                 account_holder="Test Holder",
#                 account_no="1234567899",
#                 ifsc_code="ABCD0123456",
#                 bank_type="savings",
#                 bank_branch="Test Branch",
#                 entity_type="user",
#                 user=self.user
#                 #caterer=self.catering_branch
#             )
            
#             self.assertEqual(bank_detail1.is_active, True)
            
#             bank_detail2 = BankDetails.objects.create(
#                 bank_name="Test Bank",
#                 account_holder="Test Holder",
#                 account_no="1234567890",
#                 ifsc_code="ABCD0123456",
#                 bank_type="savings",
#                 bank_branch="Test Branch",
#                 entity_type="user",
#                 user=self.user
#                 #caterer=self.catering_branch
#             )
#             bank_detail1.refresh_from_db()
#             self.assertEqual(bank_detail1.is_active,False)
#             self.assertEqual(bank_detail2.is_active,True)
            
            
#     def test_order_creation(self):
#         order = Order.objects.create(
#             user=self.user,
#             branch=self.catering_branch,
#             function_name="Wedding",
#             food_amount=5000.00,
#             gstin=18.00,
#             total_price=5900.00,
#             total_member_veg=100,
#             total_member_nonveg=50,
#             advance_paid=590.00
#         )
#         self.assertEqual(order.function_name, "Wedding")
#         self.assertEqual(order.total_price, 5900.00)
#         self.assertEqual(order.status, "pending")

#     def test_order_cancelled_items(self):
#         order = Order.objects.create(
#             user=self.user,
#             branch=self.catering_branch,
#             function_name="Birthday",
#             food_amount=3000.00,
#             gstin=18.00,
#             total_price=3540.00,
#             total_member_veg=50,
#             total_member_nonveg=25,
#             advance_paid=354.00
#         )
#         cancelled_item = CancelledOrder.objects.create(
#             order=order,
#             reason="Client Cancelled"
#         )
#         self.assertEqual(cancelled_item.reason, "Client Cancelled")
#         self.assertEqual(cancelled_item.order, order)

#     def test_delivery_creation(self):
#         order = Order.objects.create(
#             user=self.user,
#             branch=self.catering_branch,
#             function_name="Reception",
#             food_amount=6000.00,
#             gstin=18.00,
#             total_price=7080.00,
#             total_member_veg=80,
#             total_member_nonveg=40,
#             advance_paid=708.00
#         )
#         delivery = Delivery.objects.create(
#             order=order,
#             delivery_date=datetime.date(2024, 12, 12),
#             delivery_time=datetime.time(12, 0, 5),
#             delivery_charge=200.00,
#             period="day",
#             address=self.user.addresses.filter(is_active=True).first()
#         )
#         self.assertEqual(delivery.delivery_date, datetime.date(2024, 12, 12))
#         self.assertEqual(delivery.delivery_time, datetime.time(12, 0, 5))
#         self.assertEqual(delivery.delivery_charge, 200.00)
        
    
        

#     def test_ordered_food_creation(self):
#         order = Order.objects.create(
#             user=self.user,
#             branch=self.catering_branch,
#             function_name="Conference",
#             food_amount=7000.00,
#             gstin=18.00,
#             total_price=8260.00,
#             total_member_veg=70,
#             total_member_nonveg=30,
#             advance_paid=826.00
#         )
#         ordered_food = OrderedFood.objects.create(
#             order=order,
#             food=self.food
#         )
#         self.assertEqual(ordered_food.order, order)
#         self.assertEqual(ordered_food.food, self.food)
    
#     def test_caterer_food_creation(self):
        
        
#         caterer_foods = [
#             CatererFood(branch=self.catering_branch, food=self.food1, extra_cost=10.50),
#             CatererFood(branch=self.catering_branch, food=self.food2, extra_cost=15.00),
#             CatererFood(branch=self.catering_branch, food=self.food3, extra_cost=5.75),
#         ]

#         # Bulk create all the records
#         CatererFood.objects.bulk_create(caterer_foods)

#         order = Order.objects.create(
#             user=self.user,
#             branch=self.catering_branch,
#             function_name="Conference",
#             food_amount=7000.00,
#             gstin=18.00,
#             total_price=8260.00,
#             total_member_veg=70,
#             total_member_nonveg=30,
#             advance_paid=826.00
#         )
#         ordered_food = [
#             OrderedFood(order=order,food=self.food1),
#             OrderedFood(order=order,food=self.food2),  
#             OrderedFood(order=order,food=self.food3) 
#         ]
        
#         OrderedFood.objects.bulk_create(ordered_food)
        
        
#     #############  Validation Error ##########
# class CateringModelErrorTests(TestCase):  
#     def setUp(self):
#         # Set up test data for User, CateringService, and CateringBranch
#         self.user = User.objects.create_user(username="testuser", password="password")
        
#         Address.objects.create(
#                 entity_type="user",
#                 user=self.user,
#                 street="Another Street",
#                 city="Another City",
#                 zip_code="54321",
#                 state="Another State",
#                 country="IN",
#                 latitude="20.0760",
#                 longitude="73.8777"
#             )
        
#         self.catering_service = CateringService.objects.create(
#             caterer_name="Test Catering",
#             description="Test Description",
#             gstin_number="27AAAPL1234C1Z5",
#             caterer_id=self.user,
#             image="image.jpg"
#         )
#         self.catering_branch = CateringBranch.objects.create(
#             branch_id=self.catering_service,
#             branch_name="Test Branch"
#         )
#         self.catering_package = CateringPackage.objects.create(
#             branch=self.catering_branch,
#             starting_price=1000.00,
#             deliverable_area=10.0,
#             delivery_charge=100.00,
#             free_delivery_till_km=5.0,
#             gst_for_food=5.0,
#             max_order_night=10,
#             max_order_day=20,
#             type="veg",
#             advance_percentage=20.0
#         )
           
#         Address.objects.create(
#                 entity_type="caterer",
#                 branch=self.catering_branch,
#                 street="Another Street",
#                 city="Another City",
#                 zip_code="54321",
#                 state="Another State",
#                 country="IN",
#                 latitude="20.0760",
#                 longitude="73.8777"
#             )
               
#         self.food = Food.objects.create(
#             name="Test Food",
#             type_food="veg",
#             menu_catagory="veg_starter",
#             food_image="some_food.jpeg"
#         )

#         self.food1 = Food.objects.create(name="Veg Soup", type_food="veg", menu_catagory="veg_starter",food_image="some_food.jpeg")
#         self.food2 = Food.objects.create(name="Chicken Curry", type_food="non-veg", menu_catagory="nonveg_main",food_image="some_food.jpeg")
#         self.food3 = Food.objects.create(name="Fruit Juice", type_food="both", menu_catagory="juice",food_image="some_food.jpeg")
           
#     def test_address_for_caterer_creation_error(self):
#         with self.assertRaises(ValidationError):
#             caterer_address = Address.objects.create(
#             branch=self.catering_branch,
#             street="Test Street",
#             city="Test City",
#             zip_code="12345",
#             state="Test State",
#             country="IN",
#             latitude="19.0760",
#             longitude="72.8777"
#             # entity_type is missing here, which will trigger validation
#             )
            
#     def test_value_for_caterer_error(self):
#         with self.assertRaises(ValidationError):
#             self.catering_package_error = CateringPackage.objects.create(
#             branch_id=self.catering_branch, #another caterer with same id 
#             starting_price=1000.00,
#             deliverable_area=-10.0, #Negative value
#             delivery_charge=100.00,
#             free_delivery_till_km=5.0,
#             gst_for_food=5.0,
#             max_order_night=10,
#             max_order_day=20,
#             type="veg",
#             advance_percentage=200.0 #'Advance percentage cannot exceed 100%'
#             )
            
	
            
#     def test_entity_type_null_error(self):
#         with self.assertRaises(ValidationError):
#             Address.objects.create(
#                 branch=self.catering_branch,
#                 street="Test Street",
#                 city="Test City",
#                 zip_code="12345",
#                 state="Test State",
#                 country="IN",
#                 latitude="19.0760",
#                 longitude="72.877737465763475674", #'Ensure that there are no more than 11 digits in total.'
#                 entity_type="caterer",     
#                 #user=self.user       #'Only one entity can be linked at a time (user or caterer).'
#             )
        
#     def test_unique_address_for_caterer_error(self):
#         # Try to create two address for the same caterer
#         with self.assertRaises(ValidationError):
#             Address.objects.create(
#                 entity_type="caterer",
#                 branch=self.catering_branch,
#                 street="Another Street",
#                 city="Another City",
#                 zip_code="54321",
#                 state="Another State",
#                 country="IN",
#                 latitude="20.0760",
#                 longitude="73.8777"
#             )
#             Address.objects.create(         #'Address with this Caterer already exists.'
#                 entity_type="caterer",
#                 branch=self.catering_branch,
#                 street="Another Street",
#                 city="Another City",
#                 zip_code="54321",
#                 state="Another State",
#                 country="IN",
#                 latitude="90.0760",         #'latitude': ['Ensure this value is less than or equal to 90.0.']
#                 longitude="-180.8777"         #'longitude': ['Ensure this value is less than or equal to 180.0.'
#             )
            
#     def test_address_longitude_and_lattitude_precission_error(self):
#         with self.assertRaises(ValidationError):
#             Address.objects.create(         
#                     entity_type="user",
#                     user=self.user,
#                     street="Another Street",
#                     city="Another City",
#                     zip_code="54321",
#                     state="Another State",
#                     country="IN",
#                     latitude="80.0760876",         #'latitude': ['Ensure that there are no more than 6 decimal places.']
#                     longitude="80.8777455"         #'longitude': ['Ensure that there are no more than 6 decimal places.'
#                 )
            
#     def test_address_with_invalid_choice_error(self):
#         with self.assertRaises((ValueError,ValidationError)):
#             Address.objects.create(
#                 entity_type="order",    #"Value 'order' is not a valid choice."
#                 branch=self.user, # Cannot assign "<User: testuser>": "Address.caterer" must be a "CateringBranch" instance.
#                 user=self.catering_branch, # Cannot assign "<CateringBranch: CateringBranch object (1)>": "Address.user" must be a "User" instance.
#                 street="Another Street",
#                 city="Another City",
#                 zip_code="54321",
#                 state="Another State",
#                 country="IN",
#                 latitude="20.0760",
#                 longitude="73.8777"
#             )
#     def test_bank_details_creation_for_caterer_error(self):
#         with self.assertRaises((ValueError,ValidationError)):
#             bank_detail = BankDetails.objects.create(
#                 bank_name="Test Bank",
#                 account_holder="Test Holder",
#                 account_no="1234527890",
#                 ifsc_code="123456",#'Enter a valid IFSC code (e.g., ABCD0123456).
#                 bank_type="notsavings", #Value 'notsavings' is not a valid choice.
#                 bank_branch="Test Branch",
#                 # 'entity_type': ['This field cannot be blank.']
#                 branch=self.catering_branch,
#                 user=self.user  #Only one entity can be linked at a time (user or caterer
#             )
    
    
        
#     def test_caterer_food_creation_error(self):
#         with self.assertRaises(ValidationError):
#             caterer_foods = [
#                 CatererFood(branch=self.catering_branch, food=self.food1, extra_cost=-10.50),   # 'extra_cost': Ensure this value is greater than or equal to 0.
#                 CatererFood(branch=self.catering_branch, food=self.food2, extra_cost=15.00),
#                 CatererFood(branch=self.catering_branch, food=self.food3, extra_cost=5.75),
#             ]

#             # Bulk create all the records
#             CatererFood.objects.bulk_create(caterer_foods)

#             order = Order.objects.create(
#                 user=self.user,
#                 branch=self.catering_branch,
#                 function_name="Conference",
#                 food_amount=7000.00,
#                 gstin=18.00,
#                 total_price=8260.00,
#                 total_member_veg=70,
#                 total_member_nonveg=30,
#                 advance_paid=826.00
#             )
#             ordered_food = [
#                 OrderedFood(order=order,food=self.food1),
#                 OrderedFood(order=order,food=self.food),  #'food is not in the list of caterer_food'
#                 OrderedFood(order=order,food=self.food1) # UNIQUE constraint failed: catrinmodel_orderedfood.order_id, catrinmodel_orderedfood.food_id
#             ]
            
#             OrderedFood.objects.bulk_create(ordered_food)
#     def test_delivery_creation_error(self):
#         with self.assertRaises(ValidationError):
#             order = Order.objects.create(
#                 user=self.user,
#                 branch=self.catering_branch,
#                 function_name="Reception",
#                 food_amount=6000.00,
#                 gstin=18.00,
#                 total_price=7080.00,
#                 total_member_veg=80,
#                 total_member_nonveg=40,
#                 advance_paid=708.00
#             )
#             delivery = Delivery.objects.create(
#                 order=order,
#                 delivery_date=datetime.date(2024, 12, 12),
#                 delivery_time=datetime.time(12, 0, 5),
#                 delivery_charge=200.00,
#                 period="day",
#                 address=self.catering_branch.address
#             )
    

# class view_test(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser", password="password")
        
#         Address.objects.create(
#                 entity_type="user",
#                 user=self.user,
#                 street="Another Street",
#                 city="Another City",
#                 zip_code="54321",
#                 state="Another State",
#                 country="IN",
#                 latitude="20.0760",
#                 longitude="73.8777"
#             )
        
#         self.catering_service = CateringService.objects.create(
#             caterer_name="Test Catering",
#             description="Test Description",
#             gstin_number="27AAAPL1234C1Z5",
#             caterer_id=self.user,
#             image="image.jpg"
#         )
#         self.catering_branch = CateringBranch.objects.create(
#             branch_id=self.catering_service,
#             branch_name="Test Branch"
#         )
#         self.catering_package = CateringPackage.objects.create(
#             branch=self.catering_branch,
#             starting_price=1000.00,
#             deliverable_area=10.0,
#             delivery_charge=100.00,
#             free_delivery_till_km=5.0,
#             gst_for_food=5.0,
#             max_order_night=10,
#             max_order_day=20,
#             type="veg",
#             advance_percentage=20.0
#         )
           
#         Address.objects.create(
#                 entity_type="caterer",
#                 branch=self.catering_branch,
#                 street="Another Street",
#                 city="Another City",
#                 zip_code="54321",
#                 state="Another State",
#                 country="IN",
#                 latitude="20.0760",
#                 longitude="73.8777"
#             )
               
#         self.food = Food.objects.create(
#             name="Test Food",
#             type_food="veg",
#             menu_catagory="veg_starter",
#             food_image="some_food.jpeg"
#         )

#         self.food1 = Food.objects.create(name="Veg Soup", type_food="veg", menu_catagory="veg_starter",food_image="some_food.jpeg")
#         self.food2 = Food.objects.create(name="Chicken Curry", type_food="non-veg", menu_catagory="nonveg_main",food_image="some_food.jpeg")
#         self.food3 = Food.objects.create(name="Fruit Juice", type_food="both", menu_catagory="juice",food_image="some_food.jpeg")

# from django.test import TestCase
# from django.contrib.auth.models import User
# from caterer.forms import CreateUserForm,FoodForm,MenuCategoryForm,CateringServiceForm,CateringBranchForm,CateringPackageForm,AddressForm,BankDetailsForm,CancelledOrderForm,PhoneContactForm
# from .models import CateringPackage, CateringBranch
# from caterer.forms import MenuCategoryForm
# from .models import MenuCategoryDetails
# from .models import Food


# class CreateUserFormTest(TestCase):
    
#     def test_create_user_form_initial_username(self):
#         # Ensure the initial username starts with 'userid834'
#         last_user = User.objects.create(username="testuser", password="testpass")
#         form = CreateUserForm()
#         self.assertTrue(form.initial['username'].startswith("userid"))

#     def test_create_user_form_valid_data(self):
#         form = CreateUserForm()
#         data = {
#             'username':form.initial['username'],
#             'first_name': 'Test',
#             'last_name': 'User',
#             'email': 'testuser@example.com',
#             'password1': 'password123!@#',
#             'password2': 'password123!@#',
#         }
#         form = CreateUserForm(data)
#         self.assertTrue(form.is_valid(), "Form should be valid but it isn't")
#         if form.is_valid():
#             user = form.save()  # Save the user instance created by the form
#             #print(user.username)
#         else:
#             print(form.errors)  # This will print the auto-generated username
            
            
#         form1 = CreateUserForm()
#         data1 = {
#             'username':form1.initial['username'],
#             'first_name': 'Test',
#             'last_name': 'User',
#             'email': 'testuser@example.com',
#             'password1': 'password123!@#',
#             'password2': 'password123!@#',
#         }
#         form1 = CreateUserForm(data1)
#         self.assertTrue(form1.is_valid(), "Form should be valid but it isn't")
#         if form1.is_valid():
#             user1 = form1.save()  # Save the user instance created by the form
#             #print(user1.username)
#         else:
#             print(form1.errors)  # This will print the auto-generated username
        
    
#     def test_create_user_form_invalid_data(self):
#         form=CreateUserForm()
#         data = {
#             #'username field is required.'
#             'first_name': 'Test',
#             'last_name': 'User',
#             'email': 'testuserexample.com',    #'Enter a valid email address.'
#             'password1': 'password123',     
#             'password2': 'password124',  # The two password fields didn’t match
#         }
#         form = CreateUserForm(data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('email', form.errors)
#         self.assertIn('password2', form.errors)
#         self.assertIn('password2',form.errors)
        
#     def test_create_user_form_too_common_password(self):
#         form=CreateUserForm()
#         data = {
#             'username':form.initial['username'],
#             'first_name': 'Test',
#             'last_name': 'User',
#             'email': 'testuser@example.com',   
#             'password1': 'password',
#             'password2': 'password',  #'This password is too common.'
#         }
#         form = CreateUserForm(data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('password2', form.errors)
        
# from django.core.files.uploadedfile import SimpleUploadedFile
# from PIL import Image
# import io
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas

        
# def generate_test_image(color='red', size=(100, 100), image_format='JPEG'):
#     image = Image.new('RGB', size, color=color)
#     buffer = io.BytesIO()
#     image.save(buffer, format=image_format)
#     buffer.seek(0)
#     return buffer.getvalue()

# def generate_test_pdf(file_name='test_document.pdf'):
#     buffer = BytesIO()
#     c = canvas.Canvas(buffer, pagesize=letter)
#     c.drawString(100, 750, "This is a test PDF document.")
#     c.save()
#     buffer.seek(0)
#     return buffer.getvalue()


# class CatererFormTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser", password="password")
#         self.user2 = User.objects.create_user(username="testuser2", password="password")
#         self.image_content = generate_test_image() 
#         self.catering_service = CateringService.objects.create(
#             caterer_name="Test Catering",
#             description="Test Description",
#             gstin_number="27AAAPL1234C1Z5",
#             caterer_id=self.user2,
#             image="image.jpg"
#         )
#         self.catering_branch = CateringBranch.objects.create(
#             branch_id=self.catering_service,
#             branch_name="Test Branch"
#         )

#     def test_caterer_service_form_valid_data(self):
#         mock_file = SimpleUploadedFile(
#             name='test_image.jpg',
#             content=self.image_content,
#             content_type='image/jpeg'
#         )

#         data = {
#             'caterer_name': "Test Catering",
#             'description': "Test Description",
#             'gstin_number': "27AAAPL1234C1Z5",
#             'caterer_id': self.user.id,  # Use the User ID
#         }
#         files = {'image': mock_file}

#         form = CateringServiceForm(data, files)
#         print(form.errors)  # Output errors for debugging if needed
#         self.assertTrue(form.is_valid())

    
#     def test_caterer_service_form_invalid_data(self):

#         data = {
#             #No file was submitted. Check the encoding type on the form
#             'caterer_name': "", #This field is required
#             'description': "", #This field is required.
#             'gstin_number': "1234C1Z5", #Invalid GSTIN format
#             'caterer_id': "userid238435",  # Select a valid choice. That choice is not one of the available choices.
#         }
#         pdf_data = generate_test_pdf(file_name='test_document.pdf')
#         mock_file = SimpleUploadedFile(
#             name='test_document.pdf',
#             content=pdf_data,
#             content_type='application/pdf'
#         )
#         files = {'image': mock_file}  #Upload a valid image. The file you uploaded was either not an image or a corrupted image.

#         form = CateringServiceForm(data, files)
#         self.assertFalse(form.is_valid())
#         self.assertIn('caterer_name', form.errors)
#         self.assertIn('description', form.errors)
#         self.assertIn('gstin_number', form.errors)
#         self.assertIn('caterer_id', form.errors)
        
#     def test_caterer_form_fields(self):
#         form = CateringServiceForm()
#         self.assertIn('caterer_name', form.fields)
#         self.assertIn('description', form.fields)
#         self.assertIn('gstin_number', form.fields)
#         self.assertIn('caterer_id', form.fields)
    
#     def test_caterer_branch_with_valid_data(self):
#         data={
#             'branch_id' : self.catering_service,  #self.user2 does not cause error because both are same
#             'branch_name' : "udupi",
#         }
#         form = CateringBranchForm(data)
#         self.assertTrue(form.is_valid())
        
#     def test_caterer_with_multiple_branch(self):
#         data={
#             'branch_id' : self.catering_service,  
#             'branch_name' : "udupi",
#         }
#         data={
#             'branch_id' : self.catering_service, 
#             'branch_name' : "udupi", 
#         }
#         form = CateringBranchForm(data)
#         form1 = CateringBranchForm(data)
#         self.assertTrue(form.is_valid())
#         form.save()
#         self.assertFalse(form1.is_valid()) 
#         self.assertIn('__all__',form1.errors)   #Catering branch with this Branch id and Branch name already exists
        
        
#     def test_caterer_branch_form_invalid_data(self):
#         data={
#             'branch_id' : self.user,  #Select a valid choice. That choice is not one of the available choices.
#             'branch_name' : "", #This field is required.
#         }
#         form = CateringBranchForm(data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('branch_id', form.errors)
#         self.assertIn('branch_name', form.errors)
    
#     def test_caterer_Package_form_data(self):
#         data = {
#             'branch' : self.catering_branch,
#             'starting_price' : 1000.00,
#             'deliverable_area' : 10.0,
#             'delivery_charge' : 100.00,
#             'free_delivery_till_km' : 5.0,
#             'gst_for_food' : 5.0,
#             'max_order_night' : 10,
#             'max_order_day' : 20,
#             'type' : "veg",
#             'advance_percentage' : 20.0
#         }
#         form = CateringPackageForm(data)
#         self.assertTrue(form.is_valid())
        
#     def test_caterer_Package_form_invalid_data(self):
#         data = {
#             'branch' : self.catering_branch,
#             'starting_price' : 1000.00,
#             'deliverable_area' : 10.0,
#             'delivery_charge' : 100.00,
#             'free_delivery_till_km' : 5.0,
#             'gst_for_food' : 5.0,
#             'max_order_night' : 10,
#             'max_order_day' : 20,
#             'type' : "veg",
#             'advance_percentage' : 20.0
#         }
#         form = CateringPackageForm(data)
#         self.assertTrue(form.is_valid())
        
#         data = {
#             'branch' : self.user,  #Select a valid choice. That choice is not one of the available choices
#             'starting_price' : -1.00,  #Ensure this value is greater than or equal to 0
#             'deliverable_area' : -10.0, #Ensure this value is greater than or equal to 0
#             'delivery_charge' : -10.00,  #Ensure this value is greater than or equal to 0
#             'free_delivery_till_km' : -10.0,  #Ensure this value is greater than or equal to 0
#             'gst_for_food' : -10.0, #Ensure this value is greater than or equal to 0
#             'max_order_night' : -10, #Ensure this value is greater than or equal to 0
#             'max_order_day' : -10, #Ensure this value is greater than or equal to 0
#             'type' : "non",  #Select a valid choice. non is not one of the available choices
#             'advance_percentage' : 101.0  #Ensure this value is less than or equal to 100.
#         }
#         form = CateringPackageForm(data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('branch', form.errors)
#         self.assertIn('starting_price', form.errors)
#         self.assertIn('deliverable_area', form.errors)
#         self.assertIn('delivery_charge', form.errors)
#         self.assertIn('free_delivery_till_km', form.errors)
#         self.assertIn('gst_for_food', form.errors)
#         self.assertIn('max_order_night', form.errors)
#         self.assertIn('max_order_day', form.errors)
#         self.assertIn('type', form.errors)
#         self.assertIn('advance_percentage', form.errors)
        
        
        
# class AddressFormTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create(username="testuser", email="testuser@example.com")
#         self.catering_service = CateringService.objects.create(
#             caterer_name="Test Catering",
#             description="Test Description",
#             gstin_number="27AAAPL1234C1Z5",
#             caterer_id=self.user,
#             image="image.jpg"
#         )
#         self.catering_branch = CateringBranch.objects.create(
#             branch_id=self.catering_service,
#             branch_name="Test Branch")

#     def test_valid_user_address_form(self):
#         data = {
#             'entity_type': 'user',
#             'user': self.user,
#             'street': '123 Test St',
#             'city': 'Test City',
#             'zip_code': '12345',
#             'state': 'Test State',
#             'country': 'IN',
#             'latitude': 12.345678,
#             'longitude': 98.765432,
#             'is_active': True,
#             'is_exist': True,
#         }
#         form = AddressForm(data=data)
#         self.assertTrue(form.is_valid())

#     def test_valid_branch_address_form(self):
#         data = {
#             'entity_type': 'caterer',
#             'branch': self.catering_branch,
#             'street': '456 Branch Rd',
#             'city': 'Branch City',
#             'zip_code': '67890',
#             'state': 'Branch State',
#             'country': 'US',
#             'latitude': 45.678901,
#             'longitude': -120.567890,
#             'is_active': True,
#             'is_exist': True,
#         }
#         form = AddressForm(data=data)
#         self.assertTrue(form.is_valid())

#     def test_invalid_latitude_in_form(self):
#         data = {
#             'entity_type': 'user',
#             'user': self.user,
#             'street': 'Invalid Lat St',
#             'city': 'Invalid City',
#             'zip_code': '00000',
#             'state': 'Invalid State',
#             'country': 'IN',
#             'latitude': 10.0457566,   #Ensure that there are no more than 6 decimal places 
#             'longitude': 50.0476756,   #Ensure that there are no more than 6 decimal places
#         }
#         form = AddressForm(data=data)
        
#         self.assertFalse(form.is_valid())
#         self.assertIn('latitude', form.errors)
#         self.assertIn('longitude', form.errors)

#     def test_invalid_longitude_in_form(self):
#         data = {
#             'entity_type': 'user',
#             'user': self.user,
#             'street': 'Invalid Long St',
#             'city': 'Invalid City',
#             'zip_code': '00000',
#             'state': 'Invalid State',
#             'country': 'IN',
#             'latitude': 100.0,   # Ensure this value is less than or equal to 90.0
#             'longitude': 200.0,  # Ensure this value is less than or equal to 180.0
#         }
#         form = AddressForm(data=data)
        
#         self.assertFalse(form.is_valid())
#         self.assertIn('latitude', form.errors)
#         self.assertIn('longitude', form.errors)

#     def test_exclusive_relationships_in_form(self):
#         data = {
#             'entity_type': 'user',
#             'user': self.user,
#             'branch': self.catering_branch,  # Only one entity can be linked at a time (user or caterer)
#             'street': 'Conflict St',
#             'city': 'Conflict City',
#             'zip_code': '12345',
#             'state': 'Conflict State',
#             'country': 'IN',
#             'latitude': 10.0,
#             'longitude': 10.0,
#         }
#         form = AddressForm(data=data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('__all__', form.errors)  


        
# from django.test import TestCase
# from django.core.exceptions import ValidationError
# from .models import Food
# from django import forms
# from io import BytesIO
# from django.core.files.uploadedfile import InMemoryUploadedFile

# class FoodFormTestCase(TestCase):
#     def setUp(self):
#         # Setting up initial data for testing form
#         self.valid_data = {
#             'name': 'Veg Pizza',
#             'type_food': 'veg',
#             'menu_catagory': 'veg_main',
#         }
#         self.invalid_data = {
#             'name': '',  # This field is required
#             'type_food': 'invalid',  # Select a valid choice. invalid is not one of the available choices
#             'menu_catagory': 'invalid_category',  #Select a valid choice. invalid_category is not one of the available choices
#         }

#         # Mock an image file for testing image upload
#         self.image_content = generate_test_image()
#         mock_file = SimpleUploadedFile(
#             name='test_image.jpg',
#             content=self.image_content,
#             content_type='image/jpeg'
#         )
        
#         self.image_file={'food_image':mock_file}
        

#     def test_food_form_valid_data(self):
#         form = FoodForm(self.valid_data,self.image_file)
#         self.assertTrue(form.is_valid())
        
#         food = form.save()
#         self.assertEqual(food.name, 'Veg Pizza')
#         self.assertEqual(food.type_food, 'veg')
#         self.assertEqual(food.menu_catagory, 'veg_main')
#         self.assertTrue(food.food_image.name.startswith('food/test_image'))

#     def test_food_form_invalid_data(self):
#         form = FoodForm(self.invalid_data,self.image_file)
        
#         self.assertFalse(form.is_valid())
#         self.assertIn('name', form.errors)
#         self.assertIn('type_food', form.errors)
#         self.assertIn('menu_catagory', form.errors)
        

#     def test_food_form_save(self):
#         # Test saving a form with valid data
#         form = FoodForm(self.valid_data,self.image_file)
#         self.assertTrue(form.is_valid())
#         food = form.save()

#         # Ensure the food item is saved in the database
#         self.assertEqual(Food.objects.count(), 1)
#         self.assertEqual(food.name, 'Veg Pizza')


#     def test_food_form_with_invalid_image(self):
#         # Test form with invalid image file (wrong type)
#         pdf_data = generate_test_pdf(file_name='test_document.pdf')
#         mock_file = SimpleUploadedFile(
#             name='test_document.pdf',
#             content=pdf_data,
#             content_type='application/pdf'
#         )
        
#         pdf_file={'food_image':mock_file}  #Upload a valid image. The file you uploaded was either not an image or a corrupted image

#         form = FoodForm(self.valid_data,pdf_file)
#         print(form.errors)
#         self.assertFalse(form.is_valid())
#         self.assertIn('food_image', form.errors)


# class BankDetailsFormTest(TestCase):
#     def setUp(self):
#         # Create a user and a catering branch for test relationships
#         self.user = User.objects.create(username="testuser", email="testuser@example.com")
#         self.catering_service = CateringService.objects.create(
#             caterer_name="Test Catering",
#             description="Test Description",
#             gstin_number="27AAAPL1234C1Z5",
#             caterer_id=self.user,
#             image="image.jpg"
#         )
#         self.branch = CateringBranch.objects.create(
#             branch_id=self.catering_service,
#             branch_name="Test Branch")

#     def test_valid_form_user_entity(self):
#         """Test BankDetailsForm with valid data for a user entity."""
#         form_data = {
#             'bank_name': 'Test Bank',
#             'account_holder': 'John Doe',
#             'account_no': '1234567890',
#             'ifsc_code': 'ABCD0123456',
#             'bank_type': 'savings',
#             'bank_branch': 'Test Branch',
#             'entity_type': 'user',
#             'user': self.user,
#             'is_active': True,
#             'is_exist': True,
#         }
#         form = BankDetailsForm(data=form_data)
#         self.assertTrue(form.is_valid())
#         bank_details = form.save()
#         self.assertEqual(bank_details.bank_name, 'Test Bank')
#         self.assertEqual(bank_details.user, self.user)

#     def test_valid_form_caterer_entity(self):
#         """Test BankDetailsForm with valid data for a caterer entity."""
#         form_data = {
#             'bank_name': 'Test Bank',
#             'account_holder': 'Jane Doe',
#             'account_no': '9876543210',
#             'ifsc_code': 'EFGH0123456',
#             'bank_type': 'current',
#             'bank_branch': 'Another Branch',
#             'entity_type': 'caterer',
#             'branch': self.branch.id,
#             'is_active': True,
#             'is_exist': True,
#         }
#         form = BankDetailsForm(data=form_data)
#         self.assertTrue(form.is_valid())
#         bank_details = form.save()
#         self.assertEqual(bank_details.bank_name, 'Test Bank')
#         self.assertEqual(bank_details.branch, self.branch)

#     def test_invalid_ifsc_code(self):
#         """Test BankDetailsForm with an invalid IFSC code."""
#         form_data = {
#             'bank_name': 'Invalid Bank',
#             'account_holder': 'John Invalid',
#             'account_no': '1234567890',
#             'ifsc_code': 'INVALID1234',  # Invalid IFSC code
#             'bank_type': 'savings',
#             'bank_branch': 'Invalid Branch',
#             'entity_type': 'user',
#             'user': self.user.id,
#         }
#         form = BankDetailsForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('ifsc_code', form.errors)
#         self.assertEqual(
#             form.errors['ifsc_code'],
#             ['Enter a valid IFSC code (e.g., ABCD0123456).']
#         )

#     def test_missing_required_field(self):
#         """Test BankDetailsForm with missing required fields."""
#         form_data = {
#             'bank_name': '',
#             'account_holder': 'John Missing',
#             'account_no': '',  # Missing account number
#             'ifsc_code': 'ABCD0123456',
#             'bank_type': 'savings',
#             'bank_branch': 'Missing Branch',
#             'entity_type': 'user',
#             'user': self.user.id,
#         }
#         form = BankDetailsForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('bank_name', form.errors)
#         self.assertIn('account_no', form.errors)

#     def test_unique_account_per_entity(self):
#         """Test unique account number constraint for the same entity type."""
#         # Create a valid bank detail
#         BankDetails.objects.create(
#             bank_name='Test Bank',
#             account_holder='John Doe',
#             account_no='1234567890',
#             ifsc_code='ABCD0123456',
#             bank_type='savings',
#             bank_branch='Test Branch',
#             entity_type='user',
#             user=self.user,
#         )

#         # Try creating another with the same account number and entity type
#         form_data = {
#             'bank_name': 'Duplicate Bank',
#             'account_holder': 'Jane Doe',
#             'account_no': '1234567890',  # Duplicate account number
#             'ifsc_code': 'EFGH0123456',
#             'bank_type': 'current',
#             'bank_branch': 'Duplicate Branch',
#             'entity_type': 'user',
#             'user': self.user.id,
#         }
#         form = BankDetailsForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('__all__', form.errors)
#         self.assertIn('Bank details with this Account no and Entity type already exists', form.errors['__all__'][0])
        
        
# class CancelledOrderFormTest(TestCase):
#     def setUp(self):
#         # Create test data
#         self.user = User.objects.create(username="testuser", email="testuser@example.com")
#         self.catering_service = CateringService.objects.create(
#             caterer_name="Test Catering",
#             description="Test Description",
#             gstin_number="27AAAPL1234C1Z5",
#             caterer_id=self.user,
#             image="image.jpg"
#         )
#         self.branch = CateringBranch.objects.create(
#             branch_id=self.catering_service,
#             branch_name="Test Branch")

#         self.order = Order.objects.create(
#             user=self.user,
#             branch=self.branch,
#             function_name="Wedding",
#             food_amount=5000.00,
#             gstin=18.00,
#             total_price=5900.00,
#             total_member_veg=100,
#             total_member_nonveg=50,
#             advance_paid=590.00
#         )

#     def test_valid_cancelled_order_form(self):
#         """Test CancelledOrderForm with valid data."""
#         form_data = {
#             'order': self.order,
#             'reason': 'Event cancelled due to unforeseen circumstances.',
#         }
#         form = CancelledOrderForm(data=form_data)
#         self.assertTrue(form.is_valid())
#         cancelled_order = form.save()
#         self.assertEqual(cancelled_order.order, self.order)
#         self.assertEqual(cancelled_order.reason, 'Event cancelled due to unforeseen circumstances.')

#     def test_missing_reason(self):
#         """Test CancelledOrderForm with missing reason."""
#         form_data = {
#             'order': self.order.id,
#             'reason': '',  # Missing reason
#         }
#         form = CancelledOrderForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('reason', form.errors)
#         self.assertEqual(form.errors['reason'], ['This field is required.'])

#     def test_missing_order(self):
#         """Test CancelledOrderForm with missing order."""
#         form_data = {
#             'reason': 'Event cancelled due to venue unavailability.',
#         }
#         form = CancelledOrderForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('order', form.errors)
#         self.assertEqual(form.errors['order'], ['This field is required.'])

#     def test_duplicate_cancelled_order(self):
#         """Test that a CancelledOrder cannot be created for the same order twice."""
#         CancelledOrder.objects.create(
#             order=self.order,
#             reason='Initial cancellation reason.',
#         )

#         form_data = {
#             'order': self.order,
#             'reason': 'Another cancellation attempt.',
#         }
#         form = CancelledOrderForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('order', form.errors)
#         self.assertEqual(
#             form.errors['order'],
#             ['Cancelled order with this Order already exists.']
#         )
        
# class PhoneContactFormTest(TestCase):

#     def setUp(self):
#         # Create a user
#         self.user = User.objects.create(username="testuser", email="testuser@example.com")
        
#         # Create a catering service and branch
#         self.catering_service = CateringService.objects.create(
#             caterer_name="Test Catering",
#             description="Test Description",
#             gstin_number="27AAAPL1234C1Z5",
#             caterer_id=self.user,
#             image="image.jpg"
#         )
#         self.branch = CateringBranch.objects.create(
#             branch_id=self.catering_service,
#             branch_name="Test Branch"
#         )

#     def test_valid_phone_contact_form_user(self):
#         # Create a valid phone contact form for a user
#         form_data = {
#             "phone_number": "+918888888888",
#             "entity_type": "user",
#             "user": self.user.id,
#             "branch": None,
#             "contact_type": "Personal"
#         }
#         form = PhoneContactForm(data=form_data)
#         self.assertTrue(form.is_valid())
#         phone_contact = form.save()
#         self.assertEqual(phone_contact.phone_number, PhoneNumber.from_string("+918888888888", region="IN"))
#         self.assertEqual(phone_contact.entity_type, "user")
#         self.assertEqual(phone_contact.user, self.user)
#         self.assertEqual(phone_contact.contact_type, "Personal")

#     def test_valid_phone_contact_form_branch(self):
#         # Create a valid phone contact form for a branch
#         form_data = {
#             "phone_number": "+917777777777",
#             "entity_type": "caterer",
#             "user": None,
#             "branch": self.branch,
#             "contact_type": "Business"
#         }
#         form = PhoneContactForm(data=form_data)
#         self.assertTrue(form.is_valid())
#         phone_contact = form.save()
#         self.assertEqual(phone_contact.phone_number, PhoneNumber.from_string("+917777777777", region="IN"))
#         self.assertEqual(phone_contact.entity_type, "caterer")
#         self.assertEqual(phone_contact.branch, self.branch)
#         self.assertEqual(phone_contact.contact_type, "Business")

#     def test_invalid_phone_contact_form_duplicate_phone_number(self):
#         # Create a valid phone contact first
#         PhoneContact.objects.create(
#             phone_number="+918888888888",
#             entity_type="user",
#             user=self.user,
#             branch=None,
#             contact_type="Personal"
#         )

#         # Attempt to create another phone contact with the same phone number
#         form_data = {
#             "phone_number": "+918888888888",
#             "entity_type": "caterer",
#             "user": None,
#             "branch": self.branch,
#             "contact_type": "Business"
#         }
#         form = PhoneContactForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn("phone_number", form.errors)
#         self.assertEqual(form.errors["phone_number"], ["Phone contact with this Phone number already exists."])

#     def test_invalid_phone_contact_form_no_entity(self):
#         # Attempt to create a phone contact with no associated user or branch
#         form_data = {
#             "phone_number": "+919999999999",
#             "entity_type": "user",
#             "user": None,
#             "branch": None,
#             "contact_type": "Personal"
#         }
#         form = PhoneContactForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn("__all__", form.errors)
#         self.assertIn("entity_type is 'user', but no user is linked.", form.errors["__all__"])

#     def test_invalid_phone_contact_form_invalid_phone_number(self):
#         # Attempt to create a phone contact with an invalid phone number
#         form_data = {
#             "phone_number": "invalid_number",
#             "entity_type": "user",
#             "user": self.user,
#             "branch": None,
#             "contact_type": "Personal"
#         }
#         form = PhoneContactForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn("phone_number", form.errors)
#         self.assertIn("Enter a valid phone number (e.g. 074104 10123) or a number with an international call prefix.", form.errors["phone_number"])
        
        
        
# #################### views ###############################################
# ##########################################################################
# ##########################################################################
# #########################################################################



# from django.test import TestCase, RequestFactory
# from django.contrib.auth.models import User
# from django.urls import reverse
# from unittest.mock import patch  #MagicMock,
# from catrinmodel.models import CateringService, CateringBranch, Address, CateringPackage
# from caterer.views import check,menu
# from django.contrib.auth.models import User
# from catrinmodel.models import *
# from decimal import Decimal
# from caterer.CatererMethods import *
# from datetime import date, time
# from django.contrib.sessions.middleware import SessionMiddleware
# from django.http import HttpRequest



# class CheckViewTestCase(TestCase):
#     def setUp(self):
#         # Set up the request factory and test user
#         self.factory = RequestFactory()
#         self.session_data = {
#             'userlongitude': 76.6394,
#             'userlatitude': 12.9716,
#         }
#         self.user1 = User.objects.create_user(username="user1", password="password123")
#         self.user2 = User.objects.create_user(username="user2", password="password123")

#         self.caterer1 = User.objects.create_user(username="caterer1", password="password123")
#         self.caterer2 = User.objects.create_user(username="caterer2", password="password123")

#         # Creating Catering Services
#         self.catering_service1 = CateringService.objects.create(
#             caterer_name="Caterer One",
#             description="High-quality catering services",
#             gstin_number="22ABCDE1234F1Z5",
#             image="catering_service1.jpg",
#             caterer_id=self.caterer1
#         )

#         self.catering_service2 = CateringService.objects.create(
#             caterer_name="Caterer Two",
#             description="Affordable and tasty meals",
#             gstin_number="33ABCDE1234F2Z6",
#             image="catering_service1.jpg",
#             caterer_id=self.caterer2
#         )

#         # Creating Catering Branches
#         self.branch1 = CateringBranch.objects.create(branch_id=self.catering_service1, branch_name="udupi")
#         self.branch2 = CateringBranch.objects.create(branch_id=self.catering_service1, branch_name="manipal")
#         self.branch3 = CateringBranch.objects.create(branch_id=self.catering_service2, branch_name="udupi")

#         # Creating Addresses
#         self.address1 = Address.objects.create(
#             entity_type="user",
#             user=self.user1,
#             street="123 Main St",
#             city="Manglore",
#             zip_code="575001",
#             state="karnataka",
#             country="IN",
#             latitude=Decimal("12.9141"),
#             longitude=Decimal("74.8560"),
#         )

#         self.address2 = Address.objects.create(
#             entity_type="user",
#             user=self.user1,
#             street="456 Elm St",
#             city="udupi",
#             zip_code="576101",
#             state="karnataka",
#             country="IN",
#             latitude=Decimal("13.3409"),
#             longitude=Decimal("74.7421"),
#         )
#         #caterer
#         self.branch_address3 = Address.objects.create(
#             entity_type="caterer",
#             branch=self.branch1,
#             street="Caterer Branch 1 St",
#             city="udupi",
#             zip_code="576101",
#             state="karnataka",
#             country="IN",
#             latitude=Decimal("13.3409"),
#             longitude=Decimal("74.7421"),
#             is_active=True
#         )

#         self.branch_address2 = Address.objects.create(
#             entity_type="caterer",
#             branch=self.branch2,
#             street="Caterer Branch 2 St",
#             city="manipal",
#             zip_code="576104",
#             state="karnataka",
#             country="IN",
#             latitude=Decimal("13.3524"),
#             longitude=Decimal("74.7868"),
#             is_active=True
#         )
        
#         self.branch_address3 = Address.objects.create(
#             entity_type="caterer",
#             branch=self.branch3,
#             street="Caterer Branch 2 St",
#             city="udupi",
#             zip_code="576101",
#             state="karnataka",
#             country="IN",
#             latitude=Decimal("13.3409"),
#             longitude=Decimal("74.7421"),
#             is_active=True
#         )

#         # Creating Catering Packages
#         self.package1 = CateringPackage.objects.create(
#             branch=self.branch1,
#             starting_price=Decimal("500.00"),
#             deliverable_area=Decimal("10.00"),
#             delivery_charge=Decimal("50.00"),
#             free_delivery_till_km=Decimal("5.00"),
#             gst_for_food=Decimal("18.00"),
#             max_order_night=5,
#             max_order_day=10,
#             type="veg",
#             advance_percentage=Decimal("50.00"),
#             isavailable=True
#         )

#         self.package2 = CateringPackage.objects.create(
#             branch=self.branch2,
#             starting_price=Decimal("700.00"),
#             deliverable_area=Decimal("4.00"),
#             delivery_charge=Decimal("70.00"),
#             free_delivery_till_km=Decimal("7.00"),
#             gst_for_food=Decimal("18.00"),
#             max_order_night=7,
#             max_order_day=14,
#             type="non-veg",
#             advance_percentage=Decimal("60.00"),
#             isavailable=True
#         )
        
#         self.package3 = CateringPackage.objects.create(
#             branch=self.branch3,
#             starting_price=Decimal("700.00"),
#             deliverable_area=Decimal("15.00"),
#             delivery_charge=Decimal("70.00"),
#             free_delivery_till_km=Decimal("7.00"),
#             gst_for_food=Decimal("18.00"),
#             max_order_night=7,
#             max_order_day=14,
#             type="non-veg",
#             advance_percentage=Decimal("60.00"),
#             isavailable=True
#         )

#         # Creating Food
#         self.food1 = Food.objects.create(name="Pasta", type_food="veg", menu_catagory="veg_main",food_image="Pasta.jpg")
#         self.food2 = Food.objects.create(name="Chicken Curry", type_food="non-veg", menu_catagory="nonveg_main",food_image="Curry.jpg")
#         self.food3 = Food.objects.create(name="Juice", type_food="both", menu_catagory="juice",food_image="Juice.jpg")
#         self.food4 = Food.objects.create(name="Veg Noodles", type_food="veg", menu_catagory="NBRD",food_image="Noodles.jpg")
#         self.food5 = Food.objects.create(name="Cake", type_food="both", menu_catagory="dessert",food_image="Cake.jpg")

#         # Creating CatererFood
#         CatererFood.objects.bulk_create([
#             CatererFood(branch=self.branch1, food=self.food1, extra_cost=Decimal("50.00"), discription="Delicious Pasta"),
#             CatererFood(branch=self.branch1, food=self.food2, extra_cost=Decimal("70.00"), discription="Spicy Chicken Curry"),
#             CatererFood(branch=self.branch2, food=self.food4, extra_cost=Decimal("90.00"), discription="Spicy Noodles"),
#             CatererFood(branch=self.branch2, food=self.food3, extra_cost=Decimal("30.00"), discription="Fresh Juice"),
#             CatererFood(branch=self.branch2, food=self.food5, extra_cost=Decimal("60.00"), discription="Yummy Cake"),
#             CatererFood(branch=self.branch1, food=self.food3, extra_cost=Decimal("40.00"), discription="")
#         ])

#         # Creating Orders
#         self.order1 = Order.objects.create(
#             user=self.user1,
#             branch=self.branch1,
#             function_name="Birthday Party",
#             food_amount=Decimal("500.00"),
#             gstin=Decimal("90.00"),
#             total_price=Decimal("590.00"),
#             total_member_veg=5,
#             total_member_nonveg=2,
#             advance_paid=Decimal("250.00"),
#             status="pending",
#             note="Urgent delivery"
#         )

#         self.order2 = Order.objects.create(
#             user=self.user2,
#             branch=self.branch2,
#             function_name="Wedding",
#             food_amount=Decimal("1500.00"),
#             gstin=Decimal("270.00"),
#             total_price=Decimal("1770.00"),
#             total_member_veg=10,
#             total_member_nonveg=15,
#             advance_paid=Decimal("700.00"),
#             status="processing",
#             note="Large order"
#         )

#         # Creating OrderedFood
#         OrderedFood.objects.bulk_create([
#             OrderedFood(order=self.order1, food=self.food1),
#             OrderedFood(order=self.order1, food=self.food3),
#             OrderedFood(order=self.order2, food=self.food3),
#             OrderedFood(order=self.order2, food=self.food4)
#         ])

#         # Creating Delivery Details
#         Delivery.objects.create(
#             order=self.order1,
#             delivery_date=date.today(),
#             delivery_time=time(15, 0),
#             delivery_charge=Decimal("50.00"),
#             period="day",
#             delivery_note="Handle with care",
#             address=self.address1
#         )

#         Delivery.objects.create(
#             order=self.order2,
#             delivery_date=date.today(),
#             delivery_time=time(18, 0),
#             delivery_charge=Decimal("70.00"),
#             period="night",
#             delivery_note="Extra plates required",
#             address=self.address2
#         )

#         # Creating Cancelled Order
#         CancelledOrder.objects.create(order=self.order1, reason="Customer request")

#         # Creating Bank Details
#         BankDetails.objects.bulk_create([
#             BankDetails(
#                 bank_name="Bank1",
#                 account_holder="User1",
#                 account_no="1234567890",
#                 ifsc_code="ABCD0123456",
#                 bank_type="savings",
#                 entity_type="user",
#                 user=self.user1,
#                 is_active=True
#             ),
#             BankDetails(
#                 bank_name="Bank2",
#                 account_holder="Branch1",
#                 account_no="9876543210",
#                 ifsc_code="WXYZ0123456",
#                 bank_type="current",
#                 entity_type="caterer",
#                 branch=self.branch1,
#                 is_active=True
#             )
#         ])

#         # Creating Payment History
#         Payment.objects.bulk_create([
#             Payment(
#                 user=self.user1,
#                 branch=self.branch1,
#                 paid_amount=Decimal("250.00"),
#                 sender_bank=BankDetails.objects.get(account_no="1234567890"),
#                 receiver_bank=BankDetails.objects.get(account_no="9876543210")
#             ),
#             Payment(
#                 user=self.user2,
#                 branch=self.branch2,
#                 paid_amount=Decimal("700.00"),
#                 sender_bank=BankDetails.objects.get(account_no="1234567890"),
#                 receiver_bank=BankDetails.objects.get(account_no="9876543210")
#             )
#         ])

#     def add_session_to_request(self, request):
#         middleware = SessionMiddleware(lambda req: None)
#         middleware.process_request(request)
#         request.session.save()

#     @patch('caterer.views.Location.haversine')
#     def test_check_view(self, mock_haversine):
#         mock_haversine.return_value = Decimal('5.0')

#         # Simulate request
#         request = self.factory.get('/')
#         self.add_session_to_request(request)
#         user_address=self.user1.addresses.filter(is_active=True).first()  
#         request.session['userlongitude'] = user_address.longitude
#         request.session['userlatitude'] = user_address.latitude
#         request.user = self.user1

#         # Call view
#         response = check(request)
#         # Assert response
        
#         self.assertEqual(response.status_code, 200)
#         self.assertNotIn("manipal", response.content.decode())
#         self.assertNotIn("AdminPage", response.content.decode())
#         self.assertIn("udupi", response.content.decode())
#         self.assertIn("Caterer One", response.content.decode())
#         self.assertIn("Caterer Two", response.content.decode())


#     @patch('caterer.views.Location.haversine')
#     def test_check_view_exception_handling(self, mock_haversine):
#         user = self.user1  # Assuming user1 is a predefined test user
#         self.client.force_login(user)

#         # Simulate session data with an invalid longitude value
#         self.client.session['userlongitude'] = 12.9716
#         self.client.session['userlatitude'] = 72.9716
       
#         self.client.session.save()  # Save session after modification
        
#         # Make a request to the view that will trigger the exception
#         response = self.client.get(reverse('home'))

#         # Check if the response status is 500 (Internal Server Error)
#         self.assertEqual(response.status_code, 500)

#         # Check if the exception message is part of the response content
#         self.assertIn("Error:", response.content.decode())
#         self.assertIn("Error: 'userlongitude'", response.content.decode())
        
#     @patch('caterer.views.Location.haversine')
#     def test_check_caterer_view(self, mock_haversine):
#         mock_haversine.return_value = Decimal('5.0')

#         # Simulate request
#         request = self.factory.get('/')
#         self.add_session_to_request(request)
#         request.session['userlongitude'] = '77.5946'
#         request.session['userlatitude'] = '12.34274'
#         request.user = self.caterer1

#         # Call view
#         response = check(request)
#         # Assert response
        
#         self.assertEqual(response.status_code, 200)
#         self.assertNotIn("manipal", response.content.decode())
#         self.assertIn("AdminPage", response.content.decode())
#         self.assertIn("udupi", response.content.decode())
#         self.assertIn("Caterer One", response.content.decode())
#         self.assertIn("Caterer Two", response.content.decode())

#     def test_user_menu_test(self):
#         request = self.factory.get('/menu')
#         self.add_session_to_request(request)
#         request.session['branch']=self.branch1
#         request.user=self.user1
#         selected_items=self.branch1.caterer_food_details.last().pk
#         request.session['selected_items'] =[selected_items]
#         response = menu(request)
#         self.assertEqual(response.status_code, 200)
#         self.assertNotIn("Veg Noodles", response.content.decode())
#         self.assertIn("Juice", response.content.decode())
#         self.assertIn("Chicken Curry", response.content.decode())
#         self.assertIn("Pasta", response.content.decode())
#         #self.assertIn("Caterer Two", response.content.decode())
        