from django.contrib import admin
from django.urls import path
from caterer import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='api-register'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/check/', CheckAPIView.as_view(), name='api-check'),
    path('api/verify-otp/', OTPVerificationAPIView.as_view(), name='api-verify-otp'),
    path('api/forgot-password/', ForgotPasswordAPIView.as_view(), name='api-forgot-password'),
    path('api/menu/', MenuAPIView.as_view(), name='api-menu'),
    path('api/delivery/', DeliveryAPIView.as_view(), name='api-delivery'),
    path('api/address-phone/create/', AddressPhoneCreateAPIView.as_view(), name='api-address-phone-create'),
    path('api/caterer/form/', CatererFormAPIView.as_view(), name='api_caterer_form'), 
    path('api/order-details/', OrderListAPI.as_view(), name='order_details_api'),
    path('api/caterer/category/', CatererCategoryUpdateAPI.as_view()),
    path('api/food/add/', FoodCreateAPI.as_view()),
    path('api/my-orders/', MyOrdersAPI.as_view()),
    path('api/my-orders/<int:order_id>/foods/', OrderFoodItemsAPI.as_view()),
    path('api/dashboard/', DashboardAnalyticsAPI.as_view()),
    path('api/order/<int:id>/details/', FullOrderDetailsAPI.as_view()),
    path('api/menu-category/create/', MenuCategoryCreateAPI.as_view()),
]
