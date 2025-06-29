from django.shortcuts import get_object_or_404
from caterer.CatererMethods import Location,Cat_Email,Cat_Bill
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from caterer.forms import AddressForm,PhoneContactForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import datetime
from collections import defaultdict
from catrinmodel.serializers import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import pytz
from catrinmodel.models import CateringService, CateringBranch, Food, CatererFood, MenuCategoryDetails, Address, Order, OrderedFood, Delivery, MenuCategory

###########Exception#############
class EmailVerificationError(Exception):
    def __init__(self,error):
        super().__init__(f"Unable to send email: {error}")
#################################

def get_nearby_caterers(userlatitude, userlongitude):
    nearby_caterers = []
    for catering_branch in CateringBranch.objects.filter(is_active=True):
        caterer_address = catering_branch.address
        if caterer_address:
            caterer_latitude = caterer_address.latitude
            caterer_longitude = caterer_address.longitude
            distance = Location.haversine(userlatitude, userlongitude, caterer_latitude, caterer_longitude)
            if distance <= catering_branch.package_details.deliverable_area:
                nearby_caterers.append(catering_branch)
    return nearby_caterers

def is_user_caterer(user):
    return CateringService.objects.filter(caterer_id=user).exists()

def register_user(request, form):
    """
    Handles the registration logic:
    - Checks for existing email and username
    - Saves user as inactive
    - Generates verification token and sends email
    Returns a tuple (success, message)
    """
    user_email = form.cleaned_data.get('email')
    username = form.cleaned_data.get('username')

    if User.objects.filter(email=user_email).exists():
        return False, "Email is already registered."

    if User.objects.filter(username=username).exists():
        return False, "Username is already taken."

    user = form.save(commit=False)
    user.is_active = False
    user.save()

    token_generated = Cat_Email.generate_verification_token()
    request.session['token'] = token_generated
    try:
        send_verification_email(user_email, token_generated, request)
    except EmailVerificationError as e:
        return False, e

    return True, "Registration successful! Please check your email to verify your account."

def send_verification_email(user_email, verification_token,request):
    username=request.session.get('username')
    name=User.objects.get(username=username).first_name
    utc_time=timezone.now()
    ist_time=utc_time.astimezone(pytz.timezone('Asia/Kolkata'))
    request.session['minute']=ist_time.minute
    request.session['second']=ist_time.second
    
    current_time=str(timezone.now())[:-6].replace(" ","@")
    verification_link = f"http://127.0.0.1:8000/otp?token={verification_token}&time={current_time}"
    
    subject = "Verify Your Email Address"
    message = render_to_string('verification_email.html', {'verification_link': verification_link,'name':name})
    
    try:
        msg=EmailMultiAlternatives(subject, message, 'devadigaakash717@gmail.com', [user_email])
        msg.content_subtype="html"
        msg.send()
    except Exception as e:
        #print("verification exception"+e)
        #messages.info(request,"email is Incorrect")
        raise EmailVerificationError(e)
    
def authenticate_user_by_email(email, password):
    """
    Authenticate user using email and password.
    Returns (user, is_caterer, error_message)
    """
    try:
        user_obj = User.objects.filter(email=email).first()
        if not user_obj:
            return None, False, "Invalid email or password."

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            return None, False, "Invalid email or password."

        is_caterer = CateringService.objects.filter(caterer_id=user).exists()
        return user, is_caterer, None

    except Exception as e:
        return None, False, f"An error occurred: {str(e)}"
    
def verify_otp_token(request_token, session_token, username, token_time_str, validity_minutes=1):
    """
    Verify the OTP token from email against session token and time validity.
    
    Args:
        request_token (str): Token received from email (query param).
        session_token (str): Token stored in session.
        username (str): Username stored in session.
        token_time_str (str): Token generation time as string.
        validity_minutes (int): Validity window in minutes.

    Returns:
        bool: True if valid token and within time window, else False.
    """
    try:
        if request_token != session_token:
            return False
        
        token_time_str = token_time_str.replace("@", " ")
        token_start_time = datetime.strptime(token_time_str, "%Y-%m-%d %H:%M:%S.%f")
        current_time = timezone.now()

        if current_time <= (token_start_time + timedelta(minutes=validity_minutes)):
            # Activate the user
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()
            return True
        return False

    except Exception:
        return False

def process_forgot_password(email, new_password, request):
    """
    Process forgot password request:
    - Validate password
    - Update user password and deactivate account
    - Generate and send verification token email
    """
    if not User.objects.filter(email=email).exists():
        return False, "User with this email does not exist."

    try:
        validate_password(new_password)
    except ValidationError as e:
        return False, str(e)

    user = User.objects.get(email=email)
    user.set_password(new_password)
    user.is_active = False
    user.save()

    token_generated = Cat_Email.generate_verification_token()
    request.session['token'] = token_generated
    send_verification_email(email, token_generated, request)

    return True, "Verification email sent. Please check your inbox."

def delete_session_and_details(request):
    try:
        del request.session['minute']
        del request.session['second']
        del request.session['token']
    except:
        pass
    
def get_branch_menu(branch_id):
    branch = get_object_or_404(CateringBranch, pk=branch_id)
    menu_categories = MenuCategoryDetails.objects.filter(branch=branch).values_list('menu__name', flat=True).distinct()
    caterer_food = branch.caterer_food_details.all()
    return branch, menu_categories, caterer_food

def filter_food_items(branch, excluded_food_ids):
    return branch.caterer_food_details.all().exclude(pk__in=excluded_food_ids)

def get_selected_items(branch, selected_ids):
    unique_items = set(selected_ids)
    selected_items = branch.caterer_food_details.filter(pk__in=unique_items).all()
    return selected_items

def calculate_delivery_cost(branch, user_latitude, user_longitude):
    total_distance = int(Location.haversine(
        branch.address.latitude,
        branch.address.longitude,
        float(user_latitude),
        float(user_longitude)
    ))
    total_distance -= branch.package_details.free_delivery_till_km
    delivery_cost = int(total_distance * branch.package_details.delivery_charge)
    return max(delivery_cost, 0)

def calculate_bill(branch, request, selected_items):
    catbill = Cat_Bill()
    totalAmountFood = int(catbill.getTotalAmount(request, selected_items))
    delivery_cost = calculate_delivery_cost(branch, request.session['userlatitude'], request.session['userlongitude'])
    gst_amount = totalAmountFood * float(branch.package_details.gst_for_food / 100)
    totalAmount = int(totalAmountFood + delivery_cost + gst_amount)
    advanceAmount = int(totalAmount * (float(branch.package_details.advance_percentage) / 100))
    return totalAmountFood, delivery_cost, gst_amount, totalAmount, advanceAmount

def create_order_and_delivery(request, user, branch, selected_items, paid_amount, note):
    utc_time = timezone.now()
    ist_time = utc_time.astimezone(pytz.timezone('Asia/Kolkata'))  # if needed
    
    # Calculate amounts again or pass them if already calculated outside
    totalAmountFood, delivery_cost, gst_amount, totalAmount, advanceAmount = calculate_bill(branch, request, selected_items)
    
    if request.session['userZipCode'] != user.addresses.filter(is_active=True).first().zip_code:
        return None, "Zipcode mismatch"
    if paid_amount < advanceAmount:
        return None, "Paid amount less than advance"

    order_instance = Order.objects.create(
        user=user,
        branch=branch,
        function_name=request.session.get('functionName', ''),
        food_amount=totalAmountFood,
        gstin=branch.package_details.gst_for_food,
        total_price=totalAmount,
        total_member_veg=int(request.session.get('functionVegMember', 0)),
        total_member_nonveg=int(request.session.get('functionNonMember', 0)),
        advance_paid=paid_amount
    )
    delivery = Delivery.objects.create(
        order=order_instance,
        delivery_date=datetime.date(2024, 12, 12),  # You might want to get this from the form/request
        delivery_time=datetime.time(12, 0, 5),      # Same here, adjust as needed
        delivery_charge=delivery_cost,
        period="day",
        delivery_note=note,
        address=user.addresses.filter(is_active=True).first()
    )
    ordered_food_items = [
        OrderedFood(order=order_instance, food=item.food)
        for item in selected_items
    ]
    OrderedFood.objects.bulk_create(ordered_food_items)
    return order_instance, None

def delete_order_details(request):
    keys = [
        'orderDate',
        'orderTime',
        'functionName',
        'functionNonMember',
        'functionVegMember',
        'userZipCode',
        'food_item'
    ]

    # Iterate over each key and remove it if it exists
    for key in keys:
        request.session.pop(key, None)

def create_address_and_phone(data, entity_type, user=None, branch=None, use_serializers=False):
    """
    Core function to create Address and PhoneContact records.

    Params:
      - data: dict containing 'address' and 'phone' data
      - entity_type: 'user' or 'caterer'
      - user: User instance (if entity_type=='user')
      - branch: CateringBranch instance (if entity_type=='caterer')
      - use_serializers: bool, if True use DRF serializers, else use Django forms

    Returns:
      - (address_instance, phone_instance), None on success
      - (None, error_message) on failure
    """
    try:
        address_data = data.get('address')
        phone_data = data.get('phone')

        if not address_data or not phone_data:
            return None, "Address and phone data required."

        # Get coordinates
        city = address_data.get('city')
        state = address_data.get('state')
        zip_code = address_data.get('zip_code')
        latitude, longitude = Location.get_coordinates(','.join([city, state, zip_code]))
        address_data['latitude'] = float(latitude)
        address_data['longitude'] = float(longitude)

        # Set user or branch on address data
        if entity_type == 'user':
            address_data['user'] = user.id if use_serializers else user
            phone_data['user'] = user.id if use_serializers else user
        else:
            address_data['branch'] = branch.id if use_serializers else branch
            phone_data['branch'] = branch.id if use_serializers else branch

        if use_serializers:
            # Use DRF serializers for validation and saving
            address_serializer = AddressSerializer(data=address_data)
            if not address_serializer.is_valid():
                return None, f"Address errors: {address_serializer.errors}"
            address = address_serializer.save()

            phone_serializer = PhoneContactSerializer(data=phone_data)
            if not phone_serializer.is_valid():
                return None, f"Phone errors: {phone_serializer.errors}"
            phone_contact = phone_serializer.save()
        else:
            # Use Django Forms for validation and saving
            address_form = AddressForm(address_data)
            phone_form = PhoneContactForm(phone_data)

            # Initialize entity_type on forms (if needed)
            address_form.fields['entity_type'].initial = entity_type
            phone_form.fields['entity_type'].initial = entity_type

            if not address_form.is_valid():
                return None, f"Address errors: {address_form.errors}"
            if not phone_form.is_valid():
                return None, f"Phone errors: {phone_form.errors}"

            address = address_form.save()
            phone_contact = phone_form.save(commit=False)
            phone_contact.user = user if entity_type == 'user' else None
            phone_contact.branch = branch if entity_type == 'caterer' else None
            phone_contact.save()

        return (address, phone_contact), None

    except Exception as e:
        return None, str(e)
    
def save_or_update_caterer_branch(user, form):
    city = form.cleaned_data['city']
    state = form.cleaned_data['state']
    zip_code = form.cleaned_data['zip_code']

    latitude, longitude = Location.get_coordinates(','.join([city, state, zip_code]))

    caterer_instance = form.save(commit=False)
    caterer_instance.user_id = user
    caterer_instance.latitude = float(latitude)
    caterer_instance.longitude = float(longitude)

    if form.cleaned_data.get('image') and caterer_instance.image:
        caterer_instance.image.delete(save=False)

    caterer_instance.save()
    return caterer_instance

def get_filtered_sorted_orders(user, sort='id', status_filter=None, page_number=1, per_page=1):
    valid_sort_fields = ['id', 'ordered_time', 'delivery_date', 'total_price', 'status']
    sort = sort if sort in valid_sort_fields else 'id'

    caterer = get_object_or_404(User, username=user.username)
    orders = Order.objects.filter(caterer_id=caterer.id)

    if status_filter in ['pending', 'delivered']:
        orders = orders.filter(status=status_filter)

    # Sorting
    sort_map = {
        'status': '-status',
        'ordered_time': '-ordered_time',
        'delivery_date': 'delivery_date',
        'total_price': '-total_price',
        'id': '-id',
    }
    orders = orders.order_by(sort_map.get(sort, '-id'))

    # Pagination
    paginator = Paginator(orders, per_page)
    page_obj = paginator.get_page(page_number)

    return orders, page_obj

def update_menu_category_costs(user, formset_data):
    user = get_object_or_404(User, username=user)
    branch = get_object_or_404(CateringBranch, user_id=user.id)

    for form in formset_data:
        name = form['name']
        cost = form['cost']
        menu = get_object_or_404(MenuCategory, name=name)

        MenuCategoryDetails.objects.update_or_create(
            branch=branch,
            menu=menu,
            defaults={'cost': cost}
        )
        
def get_weekly_order_stats(user, is_previous=False):
    user_obj = get_object_or_404(User, username=user)
    start_date, end_date = get_recent_week_dates(is_previous)

    orders = Order.objects.filter(
        caterer_id=user_obj.id,
        ordered_time__range=(start_date, end_date)
    )

    orders_per_day = defaultdict(int)
    for order in orders:
        day = order.ordered_time.strftime('%A').lower()
        orders_per_day[day] += 1

    week_days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    return [orders_per_day[day] for day in week_days], orders

def get_recent_week_dates(previous):
    # Get today's date
    today = datetime.now(pytz.UTC)

    # Find the most recent Sunday
    days_to_sunday = (today.weekday() + 1) % 7
    recent_sunday = today - timedelta(days=days_to_sunday)

    # Find the most recent Saturday
    recent_saturday = recent_sunday + timedelta(days=6)
    
    if previous:
        previous_sunday = recent_sunday - timedelta(days=7)
        previous_saturday = recent_saturday - timedelta(days=7)
        return previous_sunday, previous_saturday
    else:
        return recent_sunday, recent_saturday
    
def get_user_orders(user):
    user_obj = get_object_or_404(User, username=user)
    return Order.objects.filter(user_id=user_obj.id)

def get_order_food_items(order_id):
    order = get_object_or_404(Order, id=order_id)
    food_items = OrderedFood.objects.filter(order=order)
    food_ids = food_items.values_list('food_id', flat=True)
    return Food.objects.filter(id__in=food_ids), order

