# catrinmodel/views.py  (or wherever you want your API views)

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status,generics, mixins,permissions
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from decimal import InvalidOperation
from rest_framework import serializers
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from django.urls import reverse
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from catrinmodel.serializers import *
from rest_framework.decorators import api_view, permission_classes
# import datetime
# import pytz
# from django.utils import timezone
import traceback
from catrinmodel.service import *

import json
from caterer.CatererMethods import Location,Cat_Email,Cat_Bill

from django.contrib.auth import authenticate, login

from caterer.forms import CreateUserForm,FoodForm,MenuCategoryItemForm,MenuCategoryForm,CateringServiceForm,CateringBranchForm,CateringPackageForm,AddressForm,PhoneContactForm
from .models import CateringService, CateringBranch, Food, CatererFood, MenuCategoryDetails, Address, Order, OrderedFood, Delivery, MenuCategory
#from .utils import Cat_Email  # Adjust imports

from django.contrib.auth import logout
#from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
import pytz
from collections import defaultdict

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token_generated = Cat_Email.generate_verification_token()
            request.session['token'] = token_generated
            send_verification_email(user.email, token_generated, request)
            return Response({"detail": "Registration successful! Please check your email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user_obj = User.objects.filter(email=user_email).first()
        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                is_caterer = CateringService.objects.filter(caterer_id=user).exists()
                request.session['is_caterer'] = is_caterer
                return Response({"detail": "Login successful"})
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class CheckAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            userlongitude = float(request.session.get('userlongitude'))
            userlatitude = float(request.session.get('userlatitude'))
            isCaterer = CateringService.objects.filter(caterer_id=request.user).exists()
            nearby_caterers = []

            for catering_branch in CateringBranch.objects.filter(is_active=True):
                if catering_branch.address:
                    caterer_latitude = catering_branch.address.latitude
                    caterer_longitude = catering_branch.address.longitude
                    distance = Location.haversine(userlatitude, userlongitude, caterer_latitude, caterer_longitude)
                    if distance <= catering_branch.package_details.deliverable_area:
                        nearby_caterers.append(catering_branch.id)  # or serialize detailed info

            return Response({
                'isCaterer': isCaterer,
                'all_caterers': nearby_caterers
            })
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OTPVerificationAPIView(APIView):
    def get(self, request):
        token_from_email = request.query_params.get('token')
        time = request.query_params.get('time')
        time = str(time).replace("@", " ")
        current_time = str(timezone.now())[:-6]
        started_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        try:
            token_original = request.session.get('token')
            if token_original == token_from_email:
                del request.session['token']
                username = request.session.get('username')
                if datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S.%f") <= (started_time + timedelta(minutes=1)):
                    user = User.objects.get(username=username)
                    user.is_active = True
                    user.save()
                    return Response({"detail": "Verification successful"})
        except Exception as e:
            pass
        delete_session_and_details(request)
        return Response({"detail": "Verification failed"}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordAPIView(APIView):
    def post(self, request):
        user_email = request.data.get('email')
        password = request.data.get('password')
        if User.objects.filter(email=user_email).exists():
            try:
                validate_password(password)
                updatePassword = User.objects.filter(email__exact=user_email).first()
                username = updatePassword.username
                updatePassword.set_password(password)
                updatePassword.is_active = False
                updatePassword.save()
                token_generated = Cat_Email.generate_verification_token()
                request.session['token'] = token_generated
                send_verification_email(user_email, token_generated, request)
                return Response({"detail": "Password reset email sent"})
            except ValidationError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Email does not exist"}, status=status.HTTP_404_NOT_FOUND)

class MenuAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        branch_id = request.session.get('branch_id')
        branch = get_object_or_404(CateringBranch, pk=branch_id)
        excluded_foods = request.session.get('selected_items', [])
        menu_categories = MenuCategoryDetails.objects.filter(branch=branch).values_list('menu__name', flat=True).distinct()
        caterer_food = branch.caterer_food_details.all().exclude(pk__in=excluded_foods)
        # Serialize your data properly here, using serializers
        return Response({
            "menu_categories": list(menu_categories),
            "available_food_items": [food.pk for food in caterer_food],  # serialize detailed info instead of just pk
            "selected_items": request.session.get('selected_items', [])
        })

    def post(self, request):
        if 'selected_items' not in request.session:
            request.session['selected_items'] = []
        request.session['selected_items'] += request.data.get('items', [])
        return Response({"detail": "Items added"}, status=status.HTTP_200_OK)

class DeliveryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        branch_id = request.session.get('branch_id')
        branch = get_object_or_404(CateringBranch, pk=branch_id)
        user = request.user
        selected_items_id = request.session.get('selected_items', [])
        selected_items = branch.caterer_food_details.filter(pk__in=selected_items_id)
        totalAmountFood, delivery_cost, gst_amount, totalAmount, advanceAmount = calculate_bill(branch, request, selected_items)

        return Response({
            'selected_items': [item.pk for item in selected_items],  # serialize if needed
            'delivery_cost': delivery_cost,
            'totalAmountFood': totalAmountFood,
            'totalAmount': totalAmount,
            'advanceAmount': advanceAmount,
        })

    def post(self, request):
        serializer = DeliverySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        branch_id = request.session.get('branch_id')
        branch = get_object_or_404(CateringBranch, pk=branch_id)
        user = request.user
        selected_items_id = request.session.get('selected_items', [])
        selected_items = branch.caterer_food_details.filter(pk__in=selected_items_id)

        paid = serializer.validated_data['amount']
        note = serializer.validated_data.get('note', '')

        order_instance, error = create_order_and_delivery(request, user, branch, selected_items, paid, note)
        if error:
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)

        delete_order_details(request)  # reset session
        return Response({"detail": "Order placed successfully"})

class AddressPhoneCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        entity_type = request.query_params.get('entity_type')
        if entity_type not in ['user', 'caterer']:
            return Response({"detail": "Invalid entity type"}, status=status.HTTP_400_BAD_REQUEST)

        if entity_type == 'caterer':
            branch_id = request.query_params.get('branch_id')
            branch = get_object_or_404(CateringBranch, pk=branch_id)
            user = None
        else:
            user = request.user
            branch = None

        data = {
            'address': request.data.get('address', {}),
            'phone': request.data.get('phone', {})
        }

        _, error = create_address_and_phone(data, entity_type, user, branch, use_serializers=True)

        if error:
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Address and phone contact created successfully"}, status=status.HTTP_201_CREATED)
    
class CatererFormAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        existing_caterer = CateringBranch.objects.filter(user_id=request.user).first()
        serializer = CateringBranchSerializer(instance=existing_caterer, data=request.data)

        if serializer.is_valid():
            form = CateringPackageForm(request.data, request.FILES, instance=existing_caterer)
            save_or_update_caterer_branch(request.user, form)
            return Response({'message': 'Caterer info saved successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sort = request.GET.get('sort', 'id')
        status = request.GET.get('status')
        page = request.GET.get('page', 1)

        orders, page_obj = get_filtered_sorted_orders(
            user=request.user,
            sort=sort,
            status_filter=status,
            page_number=page,
            per_page=10  # Customize as needed
        )
        serializer = OrderSerializer(page_obj, many=True)
        return Response({
            "orders": serializer.data,
            "total_pages": page_obj.paginator.num_pages,
            "current_page": page_obj.number
        })

    def post(self, request):
        order_id = request.data.get("id")
        order = get_object_or_404(Order, id=order_id, caterer_id=request.user.id)
        order.status = "delivered"
        order.save()
        return Response({"message": "Order marked as delivered."})
    
class CatererCategoryUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        formset_data = request.data.get('categories', [])
        if not formset_data:
            return Response({'error': 'No data provided.'}, status=400)

        update_menu_category_costs(request.user, formset_data)
        return Response({'success': 'Categories updated successfully'})

class FoodCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FoodCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Food added successfully'}, status=201)
        return Response(serializer.errors, status=400)

class MyOrdersAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = get_user_orders(request.user)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)

class OrderFoodItemsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        food_items, _ = get_order_food_items(order_id)
        serializer = FoodListSerializer(food_items, many=True)
        return Response(serializer.data)

class DashboardAnalyticsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        is_previous = request.GET.get('ispreviuos', 'false').lower() == 'true'
        orders_per_day, _ = get_weekly_order_stats(request.user, is_previous)
        return Response({'orders_per_day': orders_per_day})

class FullOrderDetailsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        order = get_object_or_404(Order, id=id)
        food_items = OrderedFood.objects.filter(order=order)
        food_ids = food_items.values_list('food_id', flat=True)
        selected_items = Food.objects.filter(id__in=food_ids)

        order_data = OrderDetailSerializer(order).data
        food_data = FoodListSerializer(selected_items, many=True).data

        return Response({
            'order': order_data,
            'foods': food_data,
            'type_choices': MenuCategory.CATEGORY_CHOICES
        })

class MenuCategoryCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MenuCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Menu category created'}, status=201)
        return Response(serializer.errors, status=400)
