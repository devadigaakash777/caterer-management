from django.test import TestCase
from django.contrib.auth.models import User
from caterer.forms import CreateUserForm,FoodForm,MenuCategoryForm,CateringServiceForm,CateringBranchForm,CateringPackageForm,AddressForm,BankDetailsForm,CancelledOrderForm,PhoneContactForm
from catrinmodel.models import CateringService, CateringBranch, Food, CatererFood, MenuCategoryDetails, Address, Order, OrderedFood,CancelledOrder,Delivery,BankDetails,PhoneContact,MenuCategory
from catrinmodel.models import CateringPackage, CateringBranch
from caterer.forms import MenuCategoryForm
from catrinmodel.models import MenuCategoryDetails
from catrinmodel.models import Food
from django.test import TestCase
from django.core.exceptions import ValidationError
from catrinmodel.models import Food
from django import forms
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from phonenumber_field.phonenumber import PhoneNumber

class CreateUserFormTest(TestCase):
    
    def test_create_user_form_initial_username(self):
        # Ensure the initial username starts with 'userid834'
        last_user = User.objects.create(username="testuser", password="testpass")
        form = CreateUserForm()
        self.assertTrue(form.initial['username'].startswith("userid"))

    def test_create_user_form_valid_data(self):
        form = CreateUserForm()
        data = {
            'username':form.initial['username'],
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'password123!@#',
            'password2': 'password123!@#',
        }
        form = CreateUserForm(data)
        self.assertTrue(form.is_valid(), "Form should be valid but it isn't")
        if form.is_valid():
            user = form.save()  # Save the user instance created by the form
            #print(user.username)
        else:
            print(form.errors)  # This will print the auto-generated username
            
            
        form1 = CreateUserForm()
        data1 = {
            'username':form1.initial['username'],
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'password123!@#',
            'password2': 'password123!@#',
        }
        form1 = CreateUserForm(data1)
        self.assertTrue(form1.is_valid(), "Form should be valid but it isn't")
        if form1.is_valid():
            user1 = form1.save()  # Save the user instance created by the form
            #print(user1.username)
        else:
            print(form1.errors)  # This will print the auto-generated username
        
    
    def test_create_user_form_invalid_data(self):
        form=CreateUserForm()
        data = {
            #'username field is required.'
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuserexample.com',    #'Enter a valid email address.'
            'password1': 'password123',     
            'password2': 'password124',  # The two password fields didn’t match
        }
        form = CreateUserForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)
        self.assertIn('password2',form.errors)
        
    def test_create_user_form_too_common_password(self):
        form=CreateUserForm()
        data = {
            'username':form.initial['username'],
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',   
            'password1': 'password',
            'password2': 'password',  #'This password is too common.'
        }
        form = CreateUserForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

        
def generate_test_image(color='red', size=(100, 100), image_format='JPEG'):
    image = Image.new('RGB', size, color=color)
    buffer = io.BytesIO()
    image.save(buffer, format=image_format)
    buffer.seek(0)
    return buffer.getvalue()

def generate_test_pdf(file_name='test_document.pdf'):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "This is a test PDF document.")
    c.save()
    buffer.seek(0)
    return buffer.getvalue()


class CatererFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.user2 = User.objects.create_user(username="testuser2", password="password")
        self.image_content = generate_test_image() 
        self.catering_service = CateringService.objects.create(
            caterer_name="Test Catering",
            description="Test Description",
            gstin_number="27AAAPL1234C1Z5",
            caterer_id=self.user2,
            image="image.jpg"
        )
        self.catering_branch = CateringBranch.objects.create(
            branch_id=self.catering_service,
            branch_name="Test Branch"
        )

    def test_caterer_service_form_valid_data(self):
        mock_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=self.image_content,
            content_type='image/jpeg'
        )

        data = {
            'caterer_name': "Test Catering",
            'description': "Test Description",
            'gstin_number': "27AAAPL1234C1Z5",
            'caterer_id': self.user.id,  # Use the User ID
        }
        files = {'image': mock_file}

        form = CateringServiceForm(data, files)
        print(form.errors)  # Output errors for debugging if needed
        self.assertTrue(form.is_valid())

    
    def test_caterer_service_form_invalid_data(self):

        data = {
            #No file was submitted. Check the encoding type on the form
            'caterer_name': "", #This field is required
            'description': "", #This field is required.
            'gstin_number': "1234C1Z5", #Invalid GSTIN format
            'caterer_id': "userid238435",  # Select a valid choice. That choice is not one of the available choices.
        }
        pdf_data = generate_test_pdf(file_name='test_document.pdf')
        mock_file = SimpleUploadedFile(
            name='test_document.pdf',
            content=pdf_data,
            content_type='application/pdf'
        )
        files = {'image': mock_file}  #Upload a valid image. The file you uploaded was either not an image or a corrupted image.

        form = CateringServiceForm(data, files)
        self.assertFalse(form.is_valid())
        self.assertIn('caterer_name', form.errors)
        self.assertIn('description', form.errors)
        self.assertIn('gstin_number', form.errors)
        self.assertIn('caterer_id', form.errors)
        
    def test_caterer_form_fields(self):
        form = CateringServiceForm()
        self.assertIn('caterer_name', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('gstin_number', form.fields)
        self.assertIn('caterer_id', form.fields)
    
    def test_caterer_branch_with_valid_data(self):
        data={
            'branch_id' : self.catering_service,  #self.user2 does not cause error because both are same
            'branch_name' : "udupi",
        }
        form = CateringBranchForm(data)
        self.assertTrue(form.is_valid())
        
    def test_caterer_with_multiple_branch(self):
        data={
            'branch_id' : self.catering_service,  
            'branch_name' : "udupi",
        }
        data={
            'branch_id' : self.catering_service, 
            'branch_name' : "udupi", 
        }
        form = CateringBranchForm(data)
        form1 = CateringBranchForm(data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertFalse(form1.is_valid()) 
        self.assertIn('__all__',form1.errors)   #Catering branch with this Branch id and Branch name already exists
        
        
    def test_caterer_branch_form_invalid_data(self):
        data={
            'branch_id' : self.user,  #Select a valid choice. That choice is not one of the available choices.
            'branch_name' : "", #This field is required.
        }
        form = CateringBranchForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('branch_id', form.errors)
        self.assertIn('branch_name', form.errors)
    
    def test_caterer_Package_form_data(self):
        data = {
            'branch' : self.catering_branch,
            'starting_price' : 1000.00,
            'deliverable_area' : 10.0,
            'delivery_charge' : 100.00,
            'free_delivery_till_km' : 5.0,
            'gst_for_food' : 5.0,
            'max_order_night' : 10,
            'max_order_day' : 20,
            'type' : "veg",
            'advance_percentage' : 20.0
        }
        form = CateringPackageForm(data)
        self.assertTrue(form.is_valid())
        
    def test_caterer_Package_form_invalid_data(self):
        data = {
            'branch' : self.catering_branch,
            'starting_price' : 1000.00,
            'deliverable_area' : 10.0,
            'delivery_charge' : 100.00,
            'free_delivery_till_km' : 5.0,
            'gst_for_food' : 5.0,
            'max_order_night' : 10,
            'max_order_day' : 20,
            'type' : "veg",
            'advance_percentage' : 20.0
        }
        form = CateringPackageForm(data)
        self.assertTrue(form.is_valid())
        
        data = {
            'branch' : self.user,  #Select a valid choice. That choice is not one of the available choices
            'starting_price' : -1.00,  #Ensure this value is greater than or equal to 0
            'deliverable_area' : -10.0, #Ensure this value is greater than or equal to 0
            'delivery_charge' : -10.00,  #Ensure this value is greater than or equal to 0
            'free_delivery_till_km' : -10.0,  #Ensure this value is greater than or equal to 0
            'gst_for_food' : -10.0, #Ensure this value is greater than or equal to 0
            'max_order_night' : -10, #Ensure this value is greater than or equal to 0
            'max_order_day' : -10, #Ensure this value is greater than or equal to 0
            'type' : "non",  #Select a valid choice. non is not one of the available choices
            'advance_percentage' : 101.0  #Ensure this value is less than or equal to 100.
        }
        form = CateringPackageForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('branch', form.errors)
        self.assertIn('starting_price', form.errors)
        self.assertIn('deliverable_area', form.errors)
        self.assertIn('delivery_charge', form.errors)
        self.assertIn('free_delivery_till_km', form.errors)
        self.assertIn('gst_for_food', form.errors)
        self.assertIn('max_order_night', form.errors)
        self.assertIn('max_order_day', form.errors)
        self.assertIn('type', form.errors)
        self.assertIn('advance_percentage', form.errors)
        
        
        
class AddressFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@example.com")
        self.catering_service = CateringService.objects.create(
            caterer_name="Test Catering",
            description="Test Description",
            gstin_number="27AAAPL1234C1Z5",
            caterer_id=self.user,
            image="image.jpg"
        )
        self.catering_branch = CateringBranch.objects.create(
            branch_id=self.catering_service,
            branch_name="Test Branch")

    def test_valid_user_address_form(self):
        data = {
            'entity_type': 'user',
            'user': self.user,
            'street': '123 Test St',
            'city': 'Test City',
            'zip_code': '12345',
            'state': 'Test State',
            'country': 'IN',
            'latitude': 12.345678,
            'longitude': 98.765432,
            'is_active': True,
            'is_exist': True,
        }
        form = AddressForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_branch_address_form(self):
        data = {
            'entity_type': 'caterer',
            'branch': self.catering_branch,
            'street': '456 Branch Rd',
            'city': 'Branch City',
            'zip_code': '67890',
            'state': 'Branch State',
            'country': 'US',
            'latitude': 45.678901,
            'longitude': -120.567890,
            'is_active': True,
            'is_exist': True,
        }
        form = AddressForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_latitude_in_form(self):
        data = {
            'entity_type': 'user',
            'user': self.user,
            'street': 'Invalid Lat St',
            'city': 'Invalid City',
            'zip_code': '00000',
            'state': 'Invalid State',
            'country': 'IN',
            'latitude': 10.0457566,   #Ensure that there are no more than 6 decimal places 
            'longitude': 50.0476756,   #Ensure that there are no more than 6 decimal places
        }
        form = AddressForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('latitude', form.errors)
        self.assertIn('longitude', form.errors)

    def test_invalid_longitude_in_form(self):
        data = {
            'entity_type': 'user',
            'user': self.user,
            'street': 'Invalid Long St',
            'city': 'Invalid City',
            'zip_code': '00000',
            'state': 'Invalid State',
            'country': 'IN',
            'latitude': 100.0,   # Ensure this value is less than or equal to 90.0
            'longitude': 200.0,  # Ensure this value is less than or equal to 180.0
        }
        form = AddressForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('latitude', form.errors)
        self.assertIn('longitude', form.errors)

    def test_exclusive_relationships_in_form(self):
        data = {
            'entity_type': 'user',
            'user': self.user,
            'branch': self.catering_branch,  # Only one entity can be linked at a time (user or caterer)
            'street': 'Conflict St',
            'city': 'Conflict City',
            'zip_code': '12345',
            'state': 'Conflict State',
            'country': 'IN',
            'latitude': 10.0,
            'longitude': 10.0,
        }
        form = AddressForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)  


        


class FoodFormTestCase(TestCase):
    def setUp(self):
        # Setting up initial data for testing form
        self.vegStarter=MenuCategory.objects.create(name="veg_starters")
        self.vegMain=MenuCategory.objects.create(name="veg_main")
        self.juice=MenuCategory.objects.create(name="juice")
        self.valid_data = {
            'name': 'Veg Pizza',
            'type_food': 'veg',
            'menu_category': self.vegMain,
        }
        self.invalid_data = {
            'name': '',  # This field is required
            'type_food': 'invalid',  # Select a valid choice. invalid is not one of the available choices
            'menu_category': 'invalid_category',  #Select a valid choice. invalid_category is not one of the available choices
        }

        # Mock an image file for testing image upload
        self.image_content = generate_test_image()
        mock_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=self.image_content,
            content_type='image/jpeg'
        )
        
        self.image_file={'food_image':mock_file}
        

    def test_food_form_valid_data(self):
        form = FoodForm(self.valid_data,self.image_file)
        self.assertTrue(form.is_valid())
        
        
        
        food = form.save()
        self.assertEqual(food.name, 'Veg Pizza')
        self.assertEqual(food.type_food, 'veg')
        self.assertEqual(food.menu_category.name, 'veg_main')
        self.assertTrue(food.food_image.name.startswith('food/test_image'))

    def test_food_form_invalid_data(self):
        form = FoodForm(self.invalid_data,self.image_file)
        
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('type_food', form.errors)
        self.assertIn('menu_category', form.errors)
        

    def test_food_form_save(self):
        # Test saving a form with valid data
        form = FoodForm(self.valid_data,self.image_file)
        self.assertTrue(form.is_valid())
        food = form.save()

        # Ensure the food item is saved in the database
        self.assertEqual(Food.objects.count(), 1)
        self.assertEqual(food.name, 'Veg Pizza')


    def test_food_form_with_invalid_image(self):
        # Test form with invalid image file (wrong type)
        pdf_data = generate_test_pdf(file_name='test_document.pdf')
        mock_file = SimpleUploadedFile(
            name='test_document.pdf',
            content=pdf_data,
            content_type='application/pdf'
        )
        
        pdf_file={'food_image':mock_file}  #Upload a valid image. The file you uploaded was either not an image or a corrupted image

        form = FoodForm(self.valid_data,pdf_file)
        print(form.errors)
        self.assertFalse(form.is_valid())
        self.assertIn('food_image', form.errors)


class BankDetailsFormTest(TestCase):
    def setUp(self):
        # Create a user and a catering branch for test relationships
        self.user = User.objects.create(username="testuser", email="testuser@example.com")
        self.catering_service = CateringService.objects.create(
            caterer_name="Test Catering",
            description="Test Description",
            gstin_number="27AAAPL1234C1Z5",
            caterer_id=self.user,
            image="image.jpg"
        )
        self.branch = CateringBranch.objects.create(
            branch_id=self.catering_service,
            branch_name="Test Branch")

    def test_valid_form_user_entity(self):
        """Test BankDetailsForm with valid data for a user entity."""
        form_data = {
            'bank_name': 'Test Bank',
            'account_holder': 'John Doe',
            'account_no': '1234567890',
            'ifsc_code': 'ABCD0123456',
            'bank_type': 'savings',
            'bank_branch': 'Test Branch',
            'entity_type': 'user',
            'user': self.user,
            'is_active': True,
            'is_exist': True,
        }
        form = BankDetailsForm(data=form_data)
        self.assertTrue(form.is_valid())
        bank_details = form.save()
        self.assertEqual(bank_details.bank_name, 'Test Bank')
        self.assertEqual(bank_details.user, self.user)

    def test_valid_form_caterer_entity(self):
        """Test BankDetailsForm with valid data for a caterer entity."""
        form_data = {
            'bank_name': 'Test Bank',
            'account_holder': 'Jane Doe',
            'account_no': '9876543210',
            'ifsc_code': 'EFGH0123456',
            'bank_type': 'current',
            'bank_branch': 'Another Branch',
            'entity_type': 'caterer',
            'branch': self.branch.id,
            'is_active': True,
            'is_exist': True,
        }
        form = BankDetailsForm(data=form_data)
        self.assertTrue(form.is_valid())
        bank_details = form.save()
        self.assertEqual(bank_details.bank_name, 'Test Bank')
        self.assertEqual(bank_details.branch, self.branch)

    def test_invalid_ifsc_code(self):
        """Test BankDetailsForm with an invalid IFSC code."""
        form_data = {
            'bank_name': 'Invalid Bank',
            'account_holder': 'John Invalid',
            'account_no': '1234567890',
            'ifsc_code': 'INVALID1234',  # Invalid IFSC code
            'bank_type': 'savings',
            'bank_branch': 'Invalid Branch',
            'entity_type': 'user',
            'user': self.user.id,
        }
        form = BankDetailsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('ifsc_code', form.errors)
        self.assertEqual(
            form.errors['ifsc_code'],
            ['Enter a valid IFSC code (e.g., ABCD0123456).']
        )

    def test_missing_required_field(self):
        """Test BankDetailsForm with missing required fields."""
        form_data = {
            'bank_name': '',
            'account_holder': 'John Missing',
            'account_no': '',  # Missing account number
            'ifsc_code': 'ABCD0123456',
            'bank_type': 'savings',
            'bank_branch': 'Missing Branch',
            'entity_type': 'user',
            'user': self.user.id,
        }
        form = BankDetailsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('bank_name', form.errors)
        self.assertIn('account_no', form.errors)

    def test_unique_account_per_entity(self):
        """Test unique account number constraint for the same entity type."""
        # Create a valid bank detail
        BankDetails.objects.create(
            bank_name='Test Bank',
            account_holder='John Doe',
            account_no='1234567890',
            ifsc_code='ABCD0123456',
            bank_type='savings',
            bank_branch='Test Branch',
            entity_type='user',
            user=self.user,
        )

        # Try creating another with the same account number and entity type
        form_data = {
            'bank_name': 'Duplicate Bank',
            'account_holder': 'Jane Doe',
            'account_no': '1234567890',  # Duplicate account number
            'ifsc_code': 'EFGH0123456',
            'bank_type': 'current',
            'bank_branch': 'Duplicate Branch',
            'entity_type': 'user',
            'user': self.user.id,
        }
        form = BankDetailsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn('Bank details with this Account no and Entity type already exists', form.errors['__all__'][0])
        
        
class CancelledOrderFormTest(TestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create(username="testuser", email="testuser@example.com")
        self.catering_service = CateringService.objects.create(
            caterer_name="Test Catering",
            description="Test Description",
            gstin_number="27AAAPL1234C1Z5",
            caterer_id=self.user,
            image="image.jpg"
        )
        self.branch = CateringBranch.objects.create(
            branch_id=self.catering_service,
            branch_name="Test Branch")

        self.order = Order.objects.create(
            user=self.user,
            branch=self.branch,
            function_name="Wedding",
            food_amount=5000.00,
            gstin=18.00,
            total_price=5900.00,
            total_member_veg=100,
            total_member_nonveg=50,
            advance_paid=590.00
        )

    def test_valid_cancelled_order_form(self):
        """Test CancelledOrderForm with valid data."""
        form_data = {
            'order': self.order,
            'reason': 'Event cancelled due to unforeseen circumstances.',
        }
        form = CancelledOrderForm(data=form_data)
        self.assertTrue(form.is_valid())
        cancelled_order = form.save()
        self.assertEqual(cancelled_order.order, self.order)
        self.assertEqual(cancelled_order.reason, 'Event cancelled due to unforeseen circumstances.')

    def test_missing_reason(self):
        """Test CancelledOrderForm with missing reason."""
        form_data = {
            'order': self.order.id,
            'reason': '',  # Missing reason
        }
        form = CancelledOrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('reason', form.errors)
        self.assertEqual(form.errors['reason'], ['This field is required.'])

    def test_missing_order(self):
        """Test CancelledOrderForm with missing order."""
        form_data = {
            'reason': 'Event cancelled due to venue unavailability.',
        }
        form = CancelledOrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('order', form.errors)
        self.assertEqual(form.errors['order'], ['This field is required.'])

    def test_duplicate_cancelled_order(self):
        """Test that a CancelledOrder cannot be created for the same order twice."""
        CancelledOrder.objects.create(
            order=self.order,
            reason='Initial cancellation reason.',
        )

        form_data = {
            'order': self.order,
            'reason': 'Another cancellation attempt.',
        }
        form = CancelledOrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('order', form.errors)
        self.assertEqual(
            form.errors['order'],
            ['Cancelled order with this Order already exists.']
        )
        
class PhoneContactFormTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create(username="testuser", email="testuser@example.com")
        
        # Create a catering service and branch
        self.catering_service = CateringService.objects.create(
            caterer_name="Test Catering",
            description="Test Description",
            gstin_number="27AAAPL1234C1Z5",
            caterer_id=self.user,
            image="image.jpg"
        )
        self.branch = CateringBranch.objects.create(
            branch_id=self.catering_service,
            branch_name="Test Branch"
        )

    def test_valid_phone_contact_form_user(self):
        # Create a valid phone contact form for a user
        form_data = {
            "phone_number": "+918888888888",
            "entity_type": "user",
            "user": self.user.id,
            "branch": None,
            "contact_type": "Personal"
        }
        form = PhoneContactForm(data=form_data)
        self.assertTrue(form.is_valid())
        phone_contact = form.save()
        self.assertEqual(phone_contact.phone_number, PhoneNumber.from_string("+918888888888", region="IN"))
        self.assertEqual(phone_contact.entity_type, "user")
        self.assertEqual(phone_contact.user, self.user)
        self.assertEqual(phone_contact.contact_type, "Personal")

    def test_valid_phone_contact_form_branch(self):
        # Create a valid phone contact form for a branch
        form_data = {
            "phone_number": "+917777777777",
            "entity_type": "caterer",
            "user": None,
            "branch": self.branch,
            "contact_type": "Business"
        }
        form = PhoneContactForm(data=form_data)
        self.assertTrue(form.is_valid())
        phone_contact = form.save()
        self.assertEqual(phone_contact.phone_number, PhoneNumber.from_string("+917777777777", region="IN"))
        self.assertEqual(phone_contact.entity_type, "caterer")
        self.assertEqual(phone_contact.branch, self.branch)
        self.assertEqual(phone_contact.contact_type, "Business")

    def test_invalid_phone_contact_form_duplicate_phone_number(self):
        # Create a valid phone contact first
        PhoneContact.objects.create(
            phone_number="+918888888888",
            entity_type="user",
            user=self.user,
            branch=None,
            contact_type="Personal"
        )

        # Attempt to create another phone contact with the same phone number
        form_data = {
            "phone_number": "+918888888888",
            "entity_type": "caterer",
            "user": None,
            "branch": self.branch,
            "contact_type": "Business"
        }
        form = PhoneContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)
        self.assertEqual(form.errors["phone_number"], ["Phone contact with this Phone number already exists."])

    def test_invalid_phone_contact_form_no_entity(self):
        # Attempt to create a phone contact with no associated user or branch
        form_data = {
            "phone_number": "+919999999999",
            "entity_type": "user",
            "user": None,
            "branch": None,
            "contact_type": "Personal"
        }
        form = PhoneContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn("entity_type is 'user', but no user is linked.", form.errors["__all__"])

    def test_invalid_phone_contact_form_invalid_phone_number(self):
        # Attempt to create a phone contact with an invalid phone number
        form_data = {
            "phone_number": "invalid_number",
            "entity_type": "user",
            "user": self.user,
            "branch": None,
            "contact_type": "Personal"
        }
        form = PhoneContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)
        self.assertIn("Enter a valid phone number (e.g. 074104 10123) or a number with an international call prefix.", form.errors["phone_number"])
        
   