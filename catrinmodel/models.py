from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator,MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from .utils import validate_exclusive_relationships,make_all_active_address_false,make_all_active_Bank_false,check_valid_food

#User=get_user_model()
    
class CateringService(models.Model):
    caterer_name = models.CharField(max_length=100)
    description = models.TextField()
    image=models.ImageField(upload_to="caterer/",null=True,default=None)
    gstin_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[A-Z0-9]{3}$',
            message='Invalid GSTIN format.',
            code='invalid_gstin'
        )]
    )
    caterer_id = models.OneToOneField(User, on_delete=models.PROTECT, related_name="caterer_details", primary_key=True)
    
    #to avoid to delete the use if he is a caterer
    
    def __str__(self):
        return f"{self.caterer_name}, {self.description}, {self.caterer_id}"

    def save(self, *args, **kwargs):
        self.full_clean()  # Automatically run validation before saving
        super().save(*args, **kwargs) 

    
    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)

class CateringBranch(models.Model):
    branch_id = models.ForeignKey(CateringService,on_delete=models.CASCADE,related_name="branches")
    branch_name = models.CharField(max_length=45)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['branch_id', 'branch_name'], name='unique_branch_name_per_catering_service'),
        ]
    def save(self, *args, **kwargs):
        self.full_clean()  # Automatically run validation before saving
        super().save(*args, **kwargs) 

class CateringPackage(models.Model):
    branch = models.OneToOneField(CateringBranch, on_delete=models.CASCADE, related_name="package_details",primary_key=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    deliverable_area = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])  
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,validators=[MinValueValidator(0)])
    free_delivery_till_km = models.DecimalField(max_digits=5, decimal_places=2, default=0 ,validators=[MinValueValidator(0)])
    gst_for_food = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    max_order_night = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    max_order_day = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    
    TYPE_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non-veg', 'Non-Vegetarian'),
        ('both', 'Both'),
    ]
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    advance_percentage = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]  
    )
    isavailable = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.starting_price}, {self.deliverable_area}, {self.free_delivery_till_km}, {self.isavailable}"
    
    def save(self, *args, **kwargs):
        if self.advance_percentage > 100:
            raise ValidationError("Advance percentage cannot exceed 100%")
        self.full_clean()  # Automatically run validation before saving
        super().save(*args, **kwargs) 

class Address(models.Model):
    ENTITY_TYPES = [
        ('user', 'User'),
        ('caterer', 'Caterer'),
    ]
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPES)
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='addresses'
    )
    branch = models.OneToOneField(
        CateringBranch,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='address'
    )
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = CountryField(default='IN')
    latitude = models.DecimalField(
        max_digits=11, 
        decimal_places=6,
        validators=[
            MinValueValidator(-90.0),  # Minimum latitude
            MaxValueValidator(90.0),   # Maximum latitude
        ]
    )
    longitude = models.DecimalField(
        max_digits=11, 
        decimal_places=6,
        validators=[
            MinValueValidator(-180.0), # Minimum longitude
            MaxValueValidator(180.0),  # Maximum longitude
        ]
    )
    is_active = models.BooleanField(default=True)
    is_exist = models.BooleanField(default=True)
    
    def clean(self):
        validate_exclusive_relationships(self)
        if self.entity_type == "user":
            make_all_active_address_false(self)

    def save(self, *args, **kwargs):
        self.clean()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}, {self.zip_code}"

class MenuCategory(models.Model):
    CATEGORY_CHOICES = [
        ('juice', 'Juice'),
        ('veg_starters', 'Veg Starters'),
        ('nonveg_starters', 'Nonveg Starters'),
        ('veg_main', 'Veg Main Course'),
        ('nonveg_main', 'Nonveg Main Course'),
        ('veg_bread_rice_noodle', 'Veg Bread/Rice/Noodle'),
        ('nonveg_bread_rice_noodle', 'Nonveg Bread/Rice/Noodle'),
        ('dessert', 'Dessert'),
    ]
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_name_display()
    
class MenuCategoryDetails(models.Model):
    branch = models.ForeignKey(CateringBranch, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    menu = models.ForeignKey('MenuCategory', on_delete=models.CASCADE, related_name='categories')
    
    def __str__(self):
        return f"{self.branch.name} - {self.menu.name} - ₹{self.cost}"

class Food(models.Model):
    name = models.CharField(max_length=20, unique=True)

    TYPE_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non-veg', 'Non-Vegetarian'),
        ('both', 'For Both Veg and NonVeg')
    ]
    type_food = models.CharField(max_length=7, choices=TYPE_CHOICES)

    menu_category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='foods')

    food_image = models.ImageField(upload_to="food/", null=True, default=None)

    def delete(self, *args, **kwargs):
        if self.food_image:
            self.food_image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
       return self.name
       
class CatererFoodManager(models.Manager):  # Inherit from models.Manager
    def bulk_create(self, objs, **kwargs):
        for obj in objs:
            obj.full_clean()  
        return super().bulk_create(objs, **kwargs)

class CatererFood(models.Model):
    branch = models.ForeignKey(CateringBranch, on_delete=models.CASCADE, related_name="caterer_food_details")
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="caterer_food_items")
    extra_cost=models.DecimalField(max_digits=5, decimal_places=2,default=0, validators=[MinValueValidator(0)])  
    discription=models.TextField(blank=True,null=True) 
    
    objects=CatererFoodManager()
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Automatically run validation before saving
        super().save(*args, **kwargs) 

class BankDetails(models.Model):
    BANK_TYPE_CHOICES = [
        ('savings', 'Savings'),
        ('current', 'Current'),
    ]

    ENTITY_TYPES = [
        ('user', 'User'),
        ('caterer', 'Caterer'),
    ]

    bank_name = models.CharField(max_length=50)
    account_holder = models.CharField(max_length=50)
    account_no = models.CharField(max_length=50, unique=True)
    ifsc_code = models.CharField(
        max_length=11,
        validators=[RegexValidator(
            regex=r'^[A-Z]{4}0[A-Z0-9]{6}$',
            message='Enter a valid IFSC code (e.g., ABCD0123456).',
            code='invalid_ifsc'
        )]
    )
    bank_type = models.CharField(max_length=10, choices=BANK_TYPE_CHOICES)
    bank_branch = models.CharField(max_length=50)
    entity_type = models.CharField(max_length=10, choices=ENTITY_TYPES)
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='bank_details'
    )
    branch = models.ForeignKey(
        CateringBranch,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='bank_details'
    )
    is_active = models.BooleanField(default=True)
    is_exist = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['account_no', 'entity_type'],
                name='unique_account_per_entity'
            )
        ]

    def clean(self):
        validate_exclusive_relationships(self)
        if self.user: #and self.user.bank_details.count() > 1:
            make_all_active_Bank_false(self,self.user)
        elif self.branch: #and self.caterer.bank_details.count() > 1:
            make_all_active_Bank_false(self,self.branch)

    def save(self, *args, **kwargs):
        self.clean()
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        entity = f"User: {self.user}" if self.user else f"Caterer: {self.branch}"
        return f"{self.bank_name} ({self.account_no}) - {entity}"
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name="user_bank_details")
    branch = models.ForeignKey(CateringBranch, on_delete=models.SET_NULL,null=True,related_name="caterer_bank_details")
    paid_time = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sender_bank = models.ForeignKey(BankDetails, related_name="sender_bank", on_delete=models.PROTECT, null=True)
    receiver_bank = models.ForeignKey(BankDetails, related_name="receiver_bank", on_delete=models.PROTECT, null=True)


    def save(self, *args, **kwargs):
        self.full_clean()  # Automatically run validation before saving
        super().save(*args, **kwargs) 

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),   
        ('shipped', 'Shipped'),     
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User,related_name="user_orders", on_delete=models.PROTECT, null=True)
    branch = models.ForeignKey(CateringBranch, related_name="caterer_orders", on_delete=models.PROTECT, null=True)
    ordered_time = models.DateTimeField(auto_now_add=True)
    function_name = models.CharField(max_length=100)
    food_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gstin = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_member_veg = models.IntegerField()
    total_member_nonveg = models.IntegerField()
    advance_paid = models.DecimalField(max_digits=10, decimal_places=2)  #use trigger to update
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    note = models.TextField(blank=True,null=True)
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Automatically run validation before saving
        super().save(*args, **kwargs) 
    
class CancelledOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="cancelled_orders")
    reason = models.TextField()
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Automatically run validation before saving
        super().save(*args, **kwargs) 

class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="delivery_details")
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=10, choices=[('day', 'Day'), ('night', 'Night')])
    delivery_note = models.TextField(null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL,null=True)
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Automatically run validation before saving
        self.clean()
        super().save(*args, **kwargs) 
        
    def clean(self):
        if self.address.entity_type != "user":
            raise ValidationError("Entered Address is not a user Address")    
        
class OrderedFoodManager(models.Manager):  # Inherit from models.Manager
    def bulk_create(self, objs, **kwargs):
        for obj in objs:
            check_valid_food(obj)
            obj.full_clean()  # Perform full validation
        return super().bulk_create(objs, **kwargs)

    
class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='food_items')
    food = models.ForeignKey(Food,on_delete=models.CASCADE)
    
    #quantity = models.IntegerField(default=1)     # Quantity of the item

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'food'], name='unique_food_per_order'),
        ]
        
    objects = OrderedFoodManager()
    # def save(self, *args, **kwargs):
    #     self.full_clean()  
    #     super().save(*args, **kwargs) 
    
  
  

    # Other branch-specific metadata
  

# class MenuCategoryDetails(models.Model):
#     juice = models.DecimalField(max_digits=10, decimal_places=2)
#     veg_starters_cost = models.DecimalField(max_digits=10, decimal_places=2)
#     nonveg_starters_cost = models.DecimalField(max_digits=10, decimal_places=2)
#     veg_main_cost = models.DecimalField(max_digits=10, decimal_places=2)
#     nonveg_main_cost = models.DecimalField(max_digits=10, decimal_places=2)
#     veg_bread_rice_noodle_cost = models.DecimalField(max_digits=10, decimal_places=2)
#     nonveg_bread_rice_noodle_cost = models.DecimalField(max_digits=10, decimal_places=2)
#     dessert_cost = models.DecimalField(max_digits=10, decimal_places=2)
#     branch = models.ForeignKey(CateringBranch, on_delete=models.CASCADE)
    
#     def save(self, *args, **kwargs):
#         self.full_clean()  # Automatically run validation before saving
#         super().save(*args, **kwargs) 


class PhoneContact(models.Model):
    ENTITY_TYPES = [
        ('user', 'User'),
        ('caterer', 'Caterer'),
    ]
    phone_number = PhoneNumberField(region='IN', unique=True)  # Ensure phone numbers are unique
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPES)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='phone_contacts'
    )
    branch = models.ForeignKey(
        CateringBranch,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='branch_phone_contacts'
    )
    contact_type = models.CharField(max_length=50,null=True,blank=True)

    def clean(self):
        validate_exclusive_relationships(self)
    def save(self, *args, **kwargs):
        self.clean()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.phone_number} ({self.entity_type})"


