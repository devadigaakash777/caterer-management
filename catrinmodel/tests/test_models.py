from django.test import TestCase,Client
from django.urls import reverse 
from django.shortcuts import render, get_object_or_404
#from caterer.CatererMethods import Location,Cat_Email,Cat_Bill
from catrinmodel.models import CateringService, CateringBranch, Food, CatererFood, MenuCategoryDetails, MenuCategory, Address, Order, OrderedFood,CancelledOrder,Delivery
from django.contrib.auth.models import User
from datetime import datetime
import decimal
from django.contrib.auth import get_user_model
from catrinmodel.models import CateringService, CateringBranch, CateringPackage, Address, Food, BankDetails, Order,PhoneContact
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
import datetime
from django_countries.fields import Country
from decimal import Decimal
from . import setup_test_data

class CateringModelTests(TestCase):
    
    def setUp(self):
        # Set up test data for User, CateringService, and CateringBranch
        self.user = User.objects.create_user(username="testuser", password="password")
        
        Address.objects.create(
                entity_type="user",
                user=self.user,
                street="Another Street",
                city="Another City",
                zip_code="54321",
                state="Another State",
                country="IN",
                latitude="20.0760",
                longitude="73.8777"
            )
        
        
        self.catering_service = CateringService.objects.create(
            caterer_name="Test Catering",
            description="Test Description",
            gstin_number="27AAAPL1234C1Z5",
            caterer_id=self.user,
            image="image.jpg"
        )
        self.catering_branch = CateringBranch.objects.create(
            branch_id=self.catering_service,
            branch_name="Test Branch"
        )
        self.catering_package = CateringPackage.objects.create(
            branch=self.catering_branch,
            starting_price=1000.00,
            deliverable_area=10.0,
            delivery_charge=100.00,
            free_delivery_till_km=5.0,
            gst_for_food=5.0,
            max_order_night=10,
            max_order_day=20,
            type="veg",
            advance_percentage=20.0
        )
           
        Address.objects.create(
                entity_type="caterer",
                branch=self.catering_branch,
                street="Another Street",
                city="Another City",
                zip_code="54321",
                state="Another State",
                country="IN",
                latitude="20.0760",
                longitude="73.8777"
            )

        self.vegStarter=MenuCategory.objects.create(name="veg_starters")
        self.nonVegMain=MenuCategory.objects.create(name="nonveg_main")
        self.juice=MenuCategory.objects.create(name="juice")
        
        self.food = Food.objects.create(
            name="Test Food",
            type_food="veg",
            menu_category=self.vegStarter,
            food_image="some_food.jpeg"
        )

        self.food1 = Food.objects.create(name="Veg Soup", type_food="veg",  menu_category=self.vegStarter,food_image="some_food.jpeg")
        self.food2 = Food.objects.create(name="Chicken Curry", type_food="non-veg",  menu_category=self.nonVegMain,food_image="some_food.jpeg")
        self.food3 = Food.objects.create(name="Fruit Juice", type_food="both",  menu_category=self.juice,food_image="some_food.jpeg")
            
    def test_catering_service_creation(self):
        self.assertEqual(self.catering_service.caterer_name, "Test Catering")
        self.assertEqual(self.catering_service.gstin_number, "27AAAPL1234C1Z5")
        self.assertEqual(self.catering_branch.branch_id.caterer_id.username,"testuser")
        self.assertEqual(self.catering_service.caterer_id, self.user)

    def test_catering_branch_creation(self):
        self.assertEqual(self.catering_branch.branch_name, "Test Branch")
        self.assertEqual(self.catering_branch.branch_id, self.catering_service)

    def test_catering_package_creation(self):
        self.assertEqual(self.catering_package.starting_price, 1000.00)
        self.assertEqual(self.catering_package.deliverable_area, 10.0)
        self.assertEqual(self.catering_package.type, "veg")

    def test_food_creation(self):
        self.assertEqual(self.food.name, "Test Food")
        self.assertEqual(self.food.type_food, "veg")
        self.assertEqual(self.food.menu_category.name, "veg_starters")
    
    def test_multiple_address_for_user(self):
            address1=Address.objects.create(
                entity_type="user",
                user=self.user,
                street="Another Street",
                city="Another City",
                zip_code="54321",
                state="Another State",
                country="IN",
                latitude="20.0760",
                longitude="73.8777"
            )
            
            self.assertEqual(address1.is_active, True)
            
            address2=Address.objects.create(         
                entity_type="user",
                user=self.user,
                street="Another Street",
                city="Another City",
                zip_code="54321",
                state="Another State",
                country="IN",
                latitude="-89.763743",
                longitude="179.834756"
            )
            address1.refresh_from_db()
            self.assertEqual(address2.longitude,Decimal('179.834756'))
            self.assertEqual(address1.is_active,False)
            self.assertEqual(address2.is_active,True)
            
    def test_address_str_representation(self):
        address = Address(
            street="789 Test Blvd",
            city="Test Town",
            state="Test Region",
            country=Country("IN"),
            zip_code = "578 109"
        )
        self.assertEqual(str(address), "789 Test Blvd, Test Town, Test Region, IN, 578 109")       
    
    
    def test_bank_details_creation_for_caterer(self):
        bank_detail = BankDetails.objects.create(
            bank_name="Test Bank",
            account_holder="Test Holder",
            account_no="1234567890",
            ifsc_code="ABCD0123456",
            bank_type="savings",
            bank_branch="Test Branch",
            entity_type="caterer",
            branch=self.catering_branch
        )
        self.assertEqual(bank_detail.bank_name, "Test Bank")
        self.assertEqual(bank_detail.account_holder, "Test Holder")
        self.assertEqual(bank_detail.account_no, "1234567890")
        
    
        
    def test_multiple_bank_for_user(self):
            bank_detail1 = BankDetails.objects.create(
                bank_name="Test Bank",
                account_holder="Test Holder",
                account_no="1234567899",
                ifsc_code="ABCD0123456",
                bank_type="savings",
                bank_branch="Test Branch",
                entity_type="user",
                user=self.user
                #caterer=self.catering_branch
            )
            
            self.assertEqual(bank_detail1.is_active, True)
            
            bank_detail2 = BankDetails.objects.create(
                bank_name="Test Bank",
                account_holder="Test Holder",
                account_no="1234567890",
                ifsc_code="ABCD0123456",
                bank_type="savings",
                bank_branch="Test Branch",
                entity_type="user",
                user=self.user
                #caterer=self.catering_branch
            )
            bank_detail1.refresh_from_db()
            self.assertEqual(bank_detail1.is_active,False)
            self.assertEqual(bank_detail2.is_active,True)
            
            
    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            branch=self.catering_branch,
            function_name="Wedding",
            food_amount=5000.00,
            gstin=18.00,
            total_price=5900.00,
            total_member_veg=100,
            total_member_nonveg=50,
            advance_paid=590.00
        )
        self.assertEqual(order.function_name, "Wedding")
        self.assertEqual(order.total_price, 5900.00)
        self.assertEqual(order.status, "pending")

    def test_order_cancelled_items(self):
        order = Order.objects.create(
            user=self.user,
            branch=self.catering_branch,
            function_name="Birthday",
            food_amount=3000.00,
            gstin=18.00,
            total_price=3540.00,
            total_member_veg=50,
            total_member_nonveg=25,
            advance_paid=354.00
        )
        cancelled_item = CancelledOrder.objects.create(
            order=order,
            reason="Client Cancelled"
        )
        self.assertEqual(cancelled_item.reason, "Client Cancelled")
        self.assertEqual(cancelled_item.order, order)

    def test_delivery_creation(self):
        order = Order.objects.create(
            user=self.user,
            branch=self.catering_branch,
            function_name="Reception",
            food_amount=6000.00,
            gstin=18.00,
            total_price=7080.00,
            total_member_veg=80,
            total_member_nonveg=40,
            advance_paid=708.00
        )
        delivery = Delivery.objects.create(
            order=order,
            delivery_date=datetime.date(2024, 12, 12),
            delivery_time=datetime.time(12, 0, 5),
            delivery_charge=200.00,
            period="day",
            address=self.user.addresses.filter(is_active=True).first()
        )
        self.assertEqual(delivery.delivery_date, datetime.date(2024, 12, 12))
        self.assertEqual(delivery.delivery_time, datetime.time(12, 0, 5))
        self.assertEqual(delivery.delivery_charge, 200.00)
        
    
        

    def test_ordered_food_creation(self):
        order = Order.objects.create(
            user=self.user,
            branch=self.catering_branch,
            function_name="Conference",
            food_amount=7000.00,
            gstin=18.00,
            total_price=8260.00,
            total_member_veg=70,
            total_member_nonveg=30,
            advance_paid=826.00
        )
        ordered_food = OrderedFood.objects.create(
            order=order,
            food=self.food
        )
        self.assertEqual(ordered_food.order, order)
        self.assertEqual(ordered_food.food, self.food)
    
    def test_caterer_food_creation(self):
        
        
        caterer_foods = [
            CatererFood(branch=self.catering_branch, food=self.food1, extra_cost=10.50),
            CatererFood(branch=self.catering_branch, food=self.food2, extra_cost=15.00),
            CatererFood(branch=self.catering_branch, food=self.food3, extra_cost=5.75),
        ]

        # Bulk create all the records
        CatererFood.objects.bulk_create(caterer_foods)

        order = Order.objects.create(
            user=self.user,
            branch=self.catering_branch,
            function_name="Conference",
            food_amount=7000.00,
            gstin=18.00,
            total_price=8260.00,
            total_member_veg=70,
            total_member_nonveg=30,
            advance_paid=826.00
        )
        ordered_food = [
            OrderedFood(order=order,food=self.food1),
            OrderedFood(order=order,food=self.food2),  
            OrderedFood(order=order,food=self.food3) 
        ]
        
        OrderedFood.objects.bulk_create(ordered_food)
        
        
    #############  Validation Error ##########
class CateringModelErrorTests(TestCase):  
    def setUp(self):
        # Set up test data for User, CateringService, and CateringBranch
        self.user = User.objects.create_user(username="testuser", password="password")
        
        self.vegStarter=MenuCategory.objects.create(name="veg_starters")
        self.nonVegMain=MenuCategory.objects.create(name="nonveg_main")
        self.juice=MenuCategory.objects.create(name="juice")
        
        Address.objects.create(
                entity_type="user",
                user=self.user,
                street="Another Street",
                city="Another City",
                zip_code="54321",
                state="Another State",
                country="IN",
                latitude="20.0760",
                longitude="73.8777"
            )
        
        self.catering_service = CateringService.objects.create(
            caterer_name="Test Catering",
            description="Test Description",
            gstin_number="27AAAPL1234C1Z5",
            caterer_id=self.user,
            image="image.jpg"
        )
        self.catering_branch = CateringBranch.objects.create(
            branch_id=self.catering_service,
            branch_name="Test Branch"
        )
        self.catering_package = CateringPackage.objects.create(
            branch=self.catering_branch,
            starting_price=1000.00,
            deliverable_area=10.0,
            delivery_charge=100.00,
            free_delivery_till_km=5.0,
            gst_for_food=5.0,
            max_order_night=10,
            max_order_day=20,
            type="veg",
            advance_percentage=20.0
        )
           
        Address.objects.create(
                entity_type="caterer",
                branch=self.catering_branch,
                street="Another Street",
                city="Another City",
                zip_code="54321",
                state="Another State",
                country="IN",
                latitude="20.0760",
                longitude="73.8777"
            )
               
        self.food = Food.objects.create(
            name="Test Food",
            type_food="veg",
            menu_category=self.vegStarter,
            food_image="some_food.jpeg"
        )

        self.food1 = Food.objects.create(name="Veg Soup", type_food="veg", menu_category=self.vegStarter,food_image="some_food.jpeg")
        self.food2 = Food.objects.create(name="Chicken Curry", type_food="non-veg", menu_category=self.nonVegMain,food_image="some_food.jpeg")
        self.food3 = Food.objects.create(name="Fruit Juice", type_food="both", menu_category=self.juice,food_image="some_food.jpeg")
           
    def test_address_for_caterer_creation_error(self):
        with self.assertRaises(ValidationError):
            caterer_address = Address.objects.create(
            branch=self.catering_branch,
            street="Test Street",
            city="Test City",
            zip_code="12345",
            state="Test State",
            country="IN",
            latitude="19.0760",
            longitude="72.8777"
            # entity_type is missing here, which will trigger validation
            )
            
    def test_value_for_caterer_error(self):
        with self.assertRaises(ValidationError):
            self.catering_package_error = CateringPackage.objects.create(
            branch_id=self.catering_branch, #another caterer with same id 
            starting_price=1000.00,
            deliverable_area=-10.0, #Negative value
            delivery_charge=100.00,
            free_delivery_till_km=5.0,
            gst_for_food=5.0,
            max_order_night=10,
            max_order_day=20,
            type="veg",
            advance_percentage=200.0 #'Advance percentage cannot exceed 100%'
            )
            
	
            
    def test_entity_type_null_error(self):
        with self.assertRaises(ValidationError):
            Address.objects.create(
                branch=self.catering_branch,
                street="Test Street",
                city="Test City",
                zip_code="12345",
                state="Test State",
                country="IN",
                latitude="19.0760",
                longitude="72.877737465763475674", #'Ensure that there are no more than 11 digits in total.'
                entity_type="caterer",     
                #user=self.user       #'Only one entity can be linked at a time (user or caterer).'
            )
        
    def test_unique_address_for_caterer_error(self):
        # Try to create two address for the same caterer
        with self.assertRaises(ValidationError):
            Address.objects.create(
                entity_type="caterer",
                branch=self.catering_branch,
                street="Another Street",
                city="Another City",
                zip_code="54321",
                state="Another State",
                country="IN",
                latitude="20.0760",
                longitude="73.8777"
            )
            Address.objects.create(         #'Address with this Caterer already exists.'
                entity_type="caterer",
                branch=self.catering_branch,
                street="Another Street",
                city="Another City",
                zip_code="54321",
                state="Another State",
                country="IN",
                latitude="90.0760",         #'latitude': ['Ensure this value is less than or equal to 90.0.']
                longitude="-180.8777"         #'longitude': ['Ensure this value is less than or equal to 180.0.'
            )
            
    def test_address_longitude_and_lattitude_precission_error(self):
        with self.assertRaises(ValidationError):
            Address.objects.create(         
                    entity_type="user",
                    user=self.user,
                    street="Another Street",
                    city="Another City",
                    zip_code="54321",
                    state="Another State",
                    country="IN",
                    latitude="80.0760876",         #'latitude': ['Ensure that there are no more than 6 decimal places.']
                    longitude="80.8777455"         #'longitude': ['Ensure that there are no more than 6 decimal places.'
                )
            
    def test_address_with_invalid_choice_error(self):
        with self.assertRaises((ValueError,ValidationError)):
            Address.objects.create(
                entity_type="order",    #"Value 'order' is not a valid choice."
                branch=self.user, # Cannot assign "<User: testuser>": "Address.caterer" must be a "CateringBranch" instance.
                user=self.catering_branch, # Cannot assign "<CateringBranch: CateringBranch object (1)>": "Address.user" must be a "User" instance.
                street="Another Street",
                city="Another City",
                zip_code="54321",
                state="Another State",
                country="IN",
                latitude="20.0760",
                longitude="73.8777"
            )
    def test_bank_details_creation_for_caterer_error(self):
        with self.assertRaises((ValueError,ValidationError)):
            bank_detail = BankDetails.objects.create(
                bank_name="Test Bank",
                account_holder="Test Holder",
                account_no="1234527890",
                ifsc_code="123456",#'Enter a valid IFSC code (e.g., ABCD0123456).
                bank_type="notsavings", #Value 'notsavings' is not a valid choice.
                bank_branch="Test Branch",
                # 'entity_type': ['This field cannot be blank.']
                branch=self.catering_branch,
                user=self.user  #Only one entity can be linked at a time (user or caterer
            )
    
    
        
    def test_caterer_food_creation_error(self):
        with self.assertRaises(ValidationError):
            caterer_foods = [
                CatererFood(branch=self.catering_branch, food=self.food1, extra_cost=-10.50),   # 'extra_cost': Ensure this value is greater than or equal to 0.
                CatererFood(branch=self.catering_branch, food=self.food2, extra_cost=15.00),
                CatererFood(branch=self.catering_branch, food=self.food3, extra_cost=5.75),
            ]

            # Bulk create all the records
            CatererFood.objects.bulk_create(caterer_foods)

            order = Order.objects.create(
                user=self.user,
                branch=self.catering_branch,
                function_name="Conference",
                food_amount=7000.00,
                gstin=18.00,
                total_price=8260.00,
                total_member_veg=70,
                total_member_nonveg=30,
                advance_paid=826.00
            )
            ordered_food = [
                OrderedFood(order=order,food=self.food1),
                OrderedFood(order=order,food=self.food),  #'food is not in the list of caterer_food'
                OrderedFood(order=order,food=self.food1) # UNIQUE constraint failed: catrinmodel_orderedfood.order_id, catrinmodel_orderedfood.food_id
            ]
            
            OrderedFood.objects.bulk_create(ordered_food)
    def test_delivery_creation_error(self):
        with self.assertRaises(ValidationError):
            order = Order.objects.create(
                user=self.user,
                branch=self.catering_branch,
                function_name="Reception",
                food_amount=6000.00,
                gstin=18.00,
                total_price=7080.00,
                total_member_veg=80,
                total_member_nonveg=40,
                advance_paid=708.00
            )
            delivery = Delivery.objects.create(
                order=order,
                delivery_date=datetime.date(2024, 12, 12),
                delivery_time=datetime.time(12, 0, 5),
                delivery_charge=200.00,
                period="day",
                address=self.catering_branch.address
            )
    

class view_test(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        Address.objects.create(
                entity_type="user",
                user=self.user,
                street="Another Street",
                city="Another City",
                zip_code="54321",
                state="Another State",
                country="IN",
                latitude="20.0760",
                longitude="73.8777"
            )
        
        self.catering_service = CateringService.objects.create(
            caterer_name="Test Catering",
            description="Test Description",
            gstin_number="27AAAPL1234C1Z5",
            caterer_id=self.user,
            image="image.jpg"
        )
        self.catering_branch = CateringBranch.objects.create(
            branch_id=self.catering_service,
            branch_name="Test Branch"
        )
        self.catering_package = CateringPackage.objects.create(
            branch=self.catering_branch,
            starting_price=1000.00,
            deliverable_area=10.0,
            delivery_charge=100.00,
            free_delivery_till_km=5.0,
            gst_for_food=5.0,
            max_order_night=10,
            max_order_day=20,
            type="veg",
            advance_percentage=20.0
        )
           
        Address.objects.create(
                entity_type="caterer",
                branch=self.catering_branch,
                street="Another Street",
                city="Another City",
                zip_code="54321",
                state="Another State",
                country="IN",
                latitude="20.0760",
                longitude="73.8777"
            )
        
        self.vegStarter=MenuCategory.objects.create(name="veg_starters")
        self.nonVegMain=MenuCategory.objects.create(name="nonveg_main")
        self.juice=MenuCategory.objects.create(name="juice")
        
               
        self.food = Food.objects.create(
            name="Test Food",
            type_food="veg",
            menu_category=self.vegStarter,
            food_image="some_food.jpeg"
        )

        self.food1 = Food.objects.create(name="Veg Soup", type_food="veg", menu_category=self.vegStarter,food_image="some_food.jpeg")
        self.food2 = Food.objects.create(name="Chicken Curry", type_food="non-veg", menu_category=self.nonVegMain,food_image="some_food.jpeg")
        self.food3 = Food.objects.create(name="Fruit Juice", type_food="both", menu_category=self.juice,food_image="some_food.jpeg")

class MenuCategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        Address.objects.create(
                entity_type="user",
                user=self.user,
                street="Another Street",
                city="Another City",
                zip_code="54321",
                state="Another State",
                country="IN",
                latitude="20.0760",
                longitude="73.8777"
            )
        
        self.catering_service = CateringService.objects.create(
            caterer_name="Test Catering",
            description="Test Description",
            gstin_number="27AAAPL1234C1Z5",
            caterer_id=self.user,
            image="image.jpg"
        )
        self.catering_branch = CateringBranch.objects.create(
            branch_id=self.catering_service,
            branch_name="Test Branch"
        )
        self.catering_package = CateringPackage.objects.create(
            branch=self.catering_branch,
            starting_price=1000.00,
            deliverable_area=10.0,
            delivery_charge=100.00,
            free_delivery_till_km=5.0,
            gst_for_food=5.0,
            max_order_night=10,
            max_order_day=20,
            type="veg",
            advance_percentage=20.0
        )
           
        Address.objects.create(
                entity_type="caterer",
                branch=self.catering_branch,
                street="Another Street",
                city="Another City",
                zip_code="54321",
                state="Another State",
                country="IN",
                latitude="20.0760",
                longitude="73.8777"
            )
        self.menu_category = MenuCategory.objects.create(name="veg_starters")

    def test_negative_cost_raises_validation_error(self):
        detail = MenuCategoryDetails(
            branch=self.catering_branch,
            cost=-10.00,
            menu=self.menu_category
        )
        with self.assertRaises(ValidationError):
            detail.full_clean()

    def test_missing_menu_raises_validation_error(self):
        detail = MenuCategoryDetails(
            branch=self.catering_branch,
            menu_id=9999,  # non-existent menu
            cost=100.00
        )
        with self.assertRaises(ValidationError):
            detail.full_clean()

    def test_valid_menu_category_details_creation(self):
        detail = MenuCategoryDetails(
            branch=self.catering_branch,
            menu=self.menu_category,
            cost=150.00
        )
        try:
            detail.full_clean()  # should not raise
        except ValidationError:
            self.fail("Valid MenuCategoryDetails raised ValidationError unexpectedly.")
        
        
class CategoryModelTestOfCat(TestCase):

    def test_menu_category_creation(self):
        """Test that a MenuCategory can be created and saved properly."""
        category = MenuCategory.objects.create(name="veg_starters")
        self.assertEqual(category.name, "veg_starters")
        self.assertIsInstance(category, MenuCategory)

    def test_menu_category_str(self):
        """Test the string representation of MenuCategory."""
        category = MenuCategory.objects.create(name="dessert")
        self.assertEqual(str(category), "Dessert")

    def test_menu_category_unique_name(self):
        """Test that duplicate names raise an IntegrityError."""
        MenuCategory.objects.create(name="juice")
        with self.assertRaises(Exception):  # Can be more specific: IntegrityError
            MenuCategory.objects.create(name="juice")