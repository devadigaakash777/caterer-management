# catrinmodel/test_utils.py

from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, time
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from catrinmodel.models import (
    CateringService, CateringBranch, Address, CateringPackage, Food,
    CatererFood, Order, OrderedFood, Delivery, CancelledOrder, BankDetails,
    Payment, MenuCategory, MenuCategoryDetails
)

def setup_test_data():
    """
    Safe test data setup for unit testing only.
    Raises an error if used in a non-test environment.
    """
    # --- ✅ SAFETY CHECK ---
    db_name = settings.DATABASES['default']['NAME']

    # Allow memory database and test_ prefix
    if not (
        'memory' in db_name or 
        db_name.startswith('test')
    ):
        raise ImproperlyConfigured(f"setup_test_data() is only allowed in test environment! Current DB: {db_name}")



    # if not settings.DATABASES['default']['NAME'].startswith('test'):
    #     print(">>> Using DB:", settings.DATABASES['default']['NAME'])
    #     raise ImproperlyConfigured("setup_test_data() is only allowed in a test environment!")

    # --- ✅ USERS ---
    user1 = User.objects.create_user(username="user1", password="password123")
    user2 = User.objects.create_user(username="user2", password="password123")
    user3 = User.objects.create_user(username="user3", password="password123")
    user4 = User.objects.create_user(username="user4", password="password123")


    # --- ✅ CATERING SERVICES ---
    catering_service1 = CateringService.objects.create(
        caterer_name="Caterer One",
        description="High-quality catering services",
        gstin_number="22ABCDE1234F1Z5",
        image="catering_service1.jpg",
        caterer_id=user3
    )

    catering_service2 = CateringService.objects.create(
        caterer_name="Caterer Two",
        description="Affordable and tasty meals",
        gstin_number="33ABCDE1234F2Z6",
        image="catering_service1.jpg",
        caterer_id=user4
    )


    # --- ✅ BRANCHES ---
    branch1 = CateringBranch.objects.create(branch_id=catering_service1, branch_name="udupi")
    branch2 = CateringBranch.objects.create(branch_id=catering_service1, branch_name="manipal")
    branch3 = CateringBranch.objects.create(branch_id=catering_service2, branch_name="udupi")

    # --- ✅ ADDRESSES ---
    address_1_user_1 = Address.objects.create(
        entity_type="user",
        user=user1,
        street="123 Main St",
        city="Manglore",
        zip_code="575001",
        state="karnataka",
        country="IN",
        latitude=Decimal("12.9141"),
        longitude=Decimal("74.8560"),
    )

    address_2_user_1 = Address.objects.create(
        entity_type="user",
        user=user1,
        street="456 Elm St",
        city="udupi",
        zip_code="576101",
        state="karnataka",
        country="IN",
        latitude=Decimal("13.3409"),
        longitude=Decimal("74.7421"),
    )
    
    Address.objects.create(
        entity_type="user",
        user=user2,
        street="123 Main St",
        city="Manglore",
        zip_code="575001",
        state="karnataka",
        country="IN",
        latitude=Decimal("12.9141"),
        longitude=Decimal("74.8560"),
    )
    
    Address.objects.create(
        entity_type="user",
        user=user3,
        street="123 Main St",
        city="Manglore",
        zip_code="575001",
        state="karnataka",
        country="IN",
        latitude=Decimal("12.9141"),
        longitude=Decimal("74.8560"),
    )
    # Address.objects.create(
    #     entity_type="user",
    #     user=user4,
    #     street="123 Main St",
    #     city="Manglore",
    #     zip_code="575001",
    #     state="karnataka",
    #     country="IN",
    #     latitude=Decimal("12.9141"),
    #     longitude=Decimal("74.8560"),
    # )
    #caterer
    branch_address3 = Address.objects.create(
        entity_type="caterer",
        branch=branch1,
        street="Caterer Branch 1 St",
        city="udupi",
        zip_code="576101",
        state="karnataka",
        country="IN",
        latitude=Decimal("13.3409"),
        longitude=Decimal("74.7421"),
        is_active=True
    )

    branch_address_2_user_1 = Address.objects.create(
        entity_type="caterer",
        branch=branch2,
        street="Caterer Branch 2 St",
        city="manipal",
        zip_code="576104",
        state="karnataka",
        country="IN",
        latitude=Decimal("13.3524"),
        longitude=Decimal("74.7868"),
        is_active=True
    )
    
    branch_address3 = Address.objects.create(
        entity_type="caterer",
        branch=branch3,
        street="Caterer Branch 2 St",
        city="udupi",
        zip_code="576101",
        state="karnataka",
        country="IN",
        latitude=Decimal("13.3409"),
        longitude=Decimal("74.7421"),
        is_active=True
    )


    # --- ✅ CATERING PACKAGES ---
    package1 = CateringPackage.objects.create(
        branch=branch1,
        starting_price=Decimal("500.00"),
        deliverable_area=Decimal("10.00"),
        delivery_charge=Decimal("50.00"),
        free_delivery_till_km=Decimal("5.00"),
        gst_for_food=Decimal("18.00"),
        max_order_night=5,
        max_order_day=10,
        type="veg",
        advance_percentage=Decimal("50.00"),
        isavailable=True
    )

    package2 = CateringPackage.objects.create(
        branch=branch2,
        starting_price=Decimal("700.00"),
        deliverable_area=Decimal("4.00"),
        delivery_charge=Decimal("70.00"),
        free_delivery_till_km=Decimal("7.00"),
        gst_for_food=Decimal("18.00"),
        max_order_night=7,
        max_order_day=14,
        type="non-veg",
        advance_percentage=Decimal("60.00"),
        isavailable=True
    )
    
    package3 = CateringPackage.objects.create(
        branch=branch3,
        starting_price=Decimal("700.00"),
        deliverable_area=Decimal("15.00"),
        delivery_charge=Decimal("70.00"),
        free_delivery_till_km=Decimal("7.00"),
        gst_for_food=Decimal("18.00"),
        max_order_night=7,
        max_order_day=14,
        type="non-veg",
        advance_percentage=Decimal("60.00"),
        isavailable=True
    )


    # --- ✅ MENU CATEGORIES ---
    categories = [
        'juice', 'veg_starters', 'nonveg_starters', 'veg_main',
        'nonveg_main', 'veg_bread_rice_noodle', 'nonveg_bread_rice_noodle', 'dessert'
    ]
    menu_categories = [MenuCategory.objects.get_or_create(name=cat)[0] for cat in categories]

    # --- ✅ FOODS ---
    food1 = Food.objects.create(name="Pasta", type_food="veg", menu_category=menu_categories[3], food_image="Pasta.jpg")
    food2 = Food.objects.create(name="Chicken Curry", type_food="non-veg", menu_category=menu_categories[4], food_image="Curry.jpg")
    food3 = Food.objects.create(name="Juice", type_food="both", menu_category=menu_categories[0], food_image="Juice.jpg")
    food4 = Food.objects.create(name="Veg Noodles", type_food="veg", menu_category=menu_categories[6], food_image="Noodles.jpg")
    food5 = Food.objects.create(name="Cake", type_food="both", menu_category=menu_categories[7], food_image="Cake.jpg")

    CatererFood.objects.bulk_create([
        CatererFood(branch=branch1, food=food1, extra_cost=Decimal("50.00"), discription="Delicious Pasta"),
        CatererFood(branch=branch1, food=food2, extra_cost=Decimal("70.00"), discription="Spicy Chicken Curry"),
        CatererFood(branch=branch2, food=food4, extra_cost=Decimal("90.00"), discription="Spicy Noodles"),
        CatererFood(branch=branch2, food=food3, extra_cost=Decimal("30.00"), discription="Fresh Juice"),
        CatererFood(branch=branch2, food=food5, extra_cost=Decimal("60.00"), discription="Yummy Cake"),
        CatererFood(branch=branch1, food=food3, extra_cost=Decimal("40.00"), discription="")
    ])

    MenuCategoryDetails.objects.bulk_create([
        MenuCategoryDetails(branch=branch1, menu=menu_categories[1], cost=Decimal('10.00')),
        MenuCategoryDetails(branch=branch1, menu=menu_categories[2], cost=Decimal('30.00')),
        MenuCategoryDetails(branch=branch1, menu=menu_categories[3], cost=Decimal('50.00')),
        MenuCategoryDetails(branch=branch1, menu=menu_categories[4], cost=Decimal('70.00')),
        MenuCategoryDetails(branch=branch1, menu=menu_categories[6], cost=Decimal('100.00')),
        MenuCategoryDetails(branch=branch1, menu=menu_categories[7], cost=Decimal('80.00')),
    ])

    # --- ✅ ORDERS ---
    order1 = Order.objects.create(
        user=user1, branch=branch1, function_name="Birthday Party",
        food_amount=Decimal("500.00"), gstin=Decimal("90.00"), total_price=Decimal("590.00"),
        total_member_veg=5, total_member_nonveg=2, advance_paid=Decimal("250.00"),
        status="pending", note="Urgent delivery"
    )
    order2 = Order.objects.create(
        user=user2, branch=branch2, function_name="Wedding",
        food_amount=Decimal("1500.00"), gstin=Decimal("270.00"), total_price=Decimal("1770.00"),
        total_member_veg=10, total_member_nonveg=15, advance_paid=Decimal("700.00"),
        status="processing", note="Large order"
    )

    OrderedFood.objects.bulk_create([
        OrderedFood(order=order1, food=food1),
        OrderedFood(order=order1, food=food3),
        OrderedFood(order=order2, food=food3),
        OrderedFood(order=order2, food=food4)
    ])

    Delivery.objects.create(
        order=order1, delivery_date=date.today(), delivery_time=time(15, 0),
        delivery_charge=Decimal("50.00"), period="day",
        delivery_note="Handle with care", address=address_1_user_1
    )
    Delivery.objects.create(
        order=order2, delivery_date=date.today(), delivery_time=time(18, 0),
        delivery_charge=Decimal("70.00"), period="night",
        delivery_note="Extra plates required", address=address_2_user_1
    )

    CancelledOrder.objects.create(order=order1, reason="Customer request")

    # --- ✅ BANK DETAILS ---
    BankDetails.objects.bulk_create([
        BankDetails(
            bank_name="Bank1",
            account_holder="User1",
            account_no="1234567890",
            ifsc_code="ABCD0123456",
            bank_type="savings",
            entity_type="user",
            user=user1,
            is_active=True
        ),
        BankDetails(
            bank_name="Bank2",
            account_holder="Branch1",
            account_no="9876543210",
            ifsc_code="WXYZ0123456",
            bank_type="current",
            entity_type="caterer",
            branch=branch1,
            is_active=True
        )
    ])


    # --- ✅ PAYMENTS ---
    Payment.objects.bulk_create([
        Payment(
            user=user1,
            branch=branch1,
            paid_amount=Decimal("250.00"),
            sender_bank=BankDetails.objects.get(account_no="1234567890"),
            receiver_bank=BankDetails.objects.get(account_no="9876543210")
        ),
        Payment(
            user=user2,
            branch=branch2,
            paid_amount=Decimal("700.00"),
            sender_bank=BankDetails.objects.get(account_no="1234567890"),
            receiver_bank=BankDetails.objects.get(account_no="9876543210")
        )
    ])


    return {
        "usersList": [user1, user2], "caterersList": [user3, user4],
        "catering_servicesList": [catering_service1, catering_service2],
        "branchesList": [branch1, branch2, branch3],
        "addressesList": [address_1_user_1, branch_address3, branch_address_2_user_1],
        "catering_packagesList": [package1, package2, package3],
        "foodsList": [food1, food2, food3, food4, food5],
        "caterer_foodsList": CatererFood.objects.all(),
        "ordersList": [order1, order2], "ordered_foodsList": OrderedFood.objects.all(),
        "deliveriesList": Delivery.objects.all(), "cancelled_ordersList": CancelledOrder.objects.all(),
        "bank_detailsList":  BankDetails.objects.all(),
        "paymentsList": Payment.objects.all(),
        "menuCategory": menu_categories,
    }
