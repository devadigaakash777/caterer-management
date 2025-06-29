# serializers.py
from rest_framework import serializers
# serializers.py

from rest_framework import serializers
from .models import Food, CatererFood, Order, MenuCategoryDetails, MenuCategory, Address,PhoneContact
from .models import MenuCategory, MenuCategoryDetails, Food, Order, OrderedFood, CateringBranch
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategoryDetails
        fields = ['menu']  # Adjust fields as needed

class CateringFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = CateringBranch.caterer_food_details
        fields = '__all__'

class DeliverySerializer(serializers.Serializer):
    amount = serializers.FloatField()
    note = serializers.CharField(allow_blank=True, required=False)
    
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class PhoneContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneContact
        fields = '__all__'
        
class CateringBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CateringBranch
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
from rest_framework import serializers
from .models import Food, Order, MenuCategory, OrderedFood, MenuCategoryDetails

# Serializer for creating a new food item
class FoodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

# Serializer for listing food items
class FoodListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'image', 'price', 'type']

# Serializer for order summary
class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'ordered_time', 'status', 'total_price']

# Serializer for full order details
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'ordered_time', 'status', 'total_price']

# Serializer for creating a menu category
class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'

# Serializer for updating menu category costs (used in caterer category update)
class MenuCategoryCostSerializer(serializers.Serializer):
    name = serializers.CharField()
    cost = serializers.DecimalField(max_digits=8, decimal_places=2)
