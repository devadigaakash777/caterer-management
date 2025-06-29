from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from caterer.CatererMethods import Location,Cat_Email,Cat_Bill
from django.forms import formset_factory
from caterer.forms import CreateUserForm,FoodForm,MenuCategoryItemForm,MenuCategoryForm,CateringServiceForm,CateringBranchForm,CateringPackageForm,AddressForm,PhoneContactForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from decimal import InvalidOperation #for float conversion errors
from catrinmodel.service import *
import traceback
from django.http import Http404
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def my_view(request):
    print("called my view")
    if request.method == 'POST':
        try:
            data_json = json.loads(request.body)
            key1_value = data_json.get('key1', 'default_value1')
            key2_value = data_json.get('key2', 'default_value2')
            request.session['userlatitude'] = key1_value
            request.session['userlongitude'] = key2_value
            print(key1_value, "and ", key2_value)
            return JsonResponse({'message': 'Data received', 'received_data': data_json})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=400)


@login_required(login_url='login')
def check(request):
    if request.session.get('functionName'):
        delete_order_details(request)

    try:
        userlongitude = float(request.session.get('userlongitude', 0.0))
        userlatitude = float(request.session.get('userlatitude', 0.0))
        isCaterer = CateringService.objects.filter(caterer_id=request.user).exists()

        nearby_caterers = []
        for branch in CateringBranch.objects.filter(is_active=True):
            addr = branch.address
            if addr:
                distance = Location.haversine(userlatitude, userlongitude, addr.latitude, addr.longitude)
                if distance <= branch.package_details.deliverable_area:
                    nearby_caterers.append(branch)

        return render(request, 'check.html', {
            'isCaterer': isCaterer,
            'address': "user_address",
            'all_caterers': nearby_caterers,
        })
    except (KeyError, ObjectDoesNotExist, ValueError) as e:
        print("Error is ",e)
        return HttpResponse(f"Error: {e}", status=500)


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')

            if User.objects.filter(email=user_email).exists():
                messages.error(request, "Email is already registered.")
                return redirect('register')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken.")
                return redirect('register')

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token_generated = Cat_Email.generate_verification_token()
            request.session['username'] = username
            request.session['token'] = token_generated

            send_verification_email(user, token_generated, request)
            messages.success(request, "Registration successful! Please check your email to verify your account.")
            return redirect("timer")
        else:
            messages.error(request, "Please fix the errors below.")

    return render(request, 'register.html', {'form': form})


def loginPage(request):
    request.session.pop('minute', None)
    request.session.pop('second', None)

    if request.method == 'POST':
        user_email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(email=user_email).first()
        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
        else:
            user = None

        if user is not None:
            login(request, user)
            if CateringService.objects.filter(caterer_id=user).exists():
                request.session['is_caterer'] = True
            return redirect('home')
        else:
            messages.info(request, "Username or Password is Incorrect")

    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


from django.utils import timezone
import datetime

def otpUser(request):
    token_from_email = request.GET.get('token')
    raw_time = request.GET.get('time', '').replace("@", " ")

    try:
        # Parse the raw_time and make it timezone-aware in UTC
        started_time_naive = datetime.datetime.strptime(raw_time, "%Y-%m-%d %H:%M:%S.%f")
        started_time_aware = timezone.make_aware(started_time_naive, timezone=pytz.UTC)

        token_original = request.session.get('token')
        username = request.session.get('username')

        print("original token:", token_original)
        print("email token:", token_from_email)

        if token_original == token_from_email:
            print("Both tokens match ✔")
            
            # Get current UTC time
            current_time = timezone.now()

            # Round both times to seconds for fair comparison
            current_time = current_time.replace(microsecond=0)
            started_time_aware = started_time_aware.replace(microsecond=0)

            # Compare with 1-minute expiry window
            print(f"Comparing: {current_time} <= {started_time_aware + timedelta(minutes=1)}")

            if current_time <= (started_time_aware + timedelta(minutes=1)):
                print("Verification valid. Activating user ✅")
                user = User.objects.get(username=username)
                user.is_active = True
                user.save()
                request.session.pop('token', None)
                messages.success(request, "Account verified!")
                return redirect('login')
            else:
                print("Token expired ❌")
        else:
            print("Token mismatch ❌")
    except Exception as e:
        print("otpUser exception:", e)

    delete_session_and_details(request)
    messages.error(request, "Verification failed or token expired. Please try again.")
    return redirect('register')


def send_verification_email(user, verification_token, request):
    name = user.first_name
    user_email = user.email

    ist_time = timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))
    request.session['minute'] = ist_time.minute
    request.session['second'] = ist_time.second

    current_time = str(timezone.now())[:-6].replace(" ", "@")
    verification_link = f"http://127.0.0.1:8000/otp?token={verification_token}&time={current_time}"

    subject = "Verify Your Email Address"
    message = render_to_string('verification_email.html', {
        'verification_link': verification_link,
        'name': name
    })

    try:
        msg = EmailMultiAlternatives(subject, message, 'devadigaakash717@gmail.com', [user_email])
        msg.content_subtype = "html"
        msg.send()
    except Exception as e:
        print("Email sending failed:", e)
        messages.error(request, "Could not send verification email.")
        return redirect('register')


def forgotUser(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=user_email).first()
        if user:
            try:
                validate_password(password)
                user.set_password(password)
                user.is_active = False
                user.save()

                token_generated = Cat_Email.generate_verification_token()
                request.session['username'] = user.username
                request.session['token'] = token_generated
                send_verification_email(user, token_generated, request)
                return redirect("timer")
            except ValidationError as e:
                messages.error(request, e)
        else:
            print('User with given email does not exist.')

    return render(request, "forgotPas.html")


def timer(request):
    try:
        minute = int(request.session.get('minute', 0))
        second = int(request.session.get('second', 0))
        return render(request, "timer.html", {'minute': minute, 'second': second})
    except Exception as e:
        delete_session_and_details(request)
    return render(request, "timer.html")


def delete_session_and_details(request):
    for key in ['minute', 'second', 'token']:
        request.session.pop(key, None)


def resend_link(request):
    try:
        username = request.session.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            token_generated = Cat_Email.generate_verification_token()
            request.session['token'] = token_generated
            send_verification_email(user, token_generated, request)
            return redirect("timer")
    except Exception as e:
        print(e)
    return redirect("register")


@login_required(login_url='login')
def menu(request):
    try:
        branch_id = request.session.get('branch_id')
        if not branch_id:
            return HttpResponse("Branch not found in session", status=400)

        branch, menu_categories, _ = get_branch_menu(branch_id)

        if request.method == 'POST':
            if request.POST.get('add_to_order') == "submit":
                return redirect("delivery")
            elif request.POST.get('add_item') == "add":
                if 'selected_items' not in request.session:
                    request.session['selected_items'] = []
                request.session['selected_items'] += request.POST.getlist('items')
                # Remove duplicates
                request.session['selected_items'] = list(set(request.session['selected_items']))

        excluded_foods = request.session.get('selected_items', [])

        selected_items = get_selected_items(branch, excluded_foods)
        request.session['selected_items'] = [item.pk for item in selected_items]

        caterer_food = filter_food_items(branch, excluded_foods)

        context = {
            'selected_items': selected_items,
            'record': caterer_food,
            'type': menu_categories,
        }
        return render(request, 'food_menu.html', context)

    except Http404 as e:
        return HttpResponse(f"Error: {e}", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)

def remove(request):
    food_list=[]
    if(request.method == 'GET'):
        item_to_remove=request.GET.get("delete")
        food_list = request.session.get('selected_items', [])
        food_list.remove(item_to_remove)
        request.session['selected_items'] = food_list
        print(item_to_remove)
        return redirect("menu")
    
@login_required(login_url='login')
def order(request):
    if(request.method == 'GET'):
        request.session['branch_id'] = request.GET.get("branch")
    if(request.method == 'POST'):
        request.session['orderDate']=request.POST.get("orderDate")
        request.session['orderTime']=request.POST.get("orderTime")
        request.session['functionName']=request.POST.get("functionName")
        request.session['functionNonMember']=request.POST.get("functionNonMember")
        request.session['functionVegMember']=request.POST.get("functionVegMember")
        request.session['userZipCode']=request.POST.get("zip")
        return redirect("menu")
    context={}
    return render(request, 'order.html', context)

@login_required(login_url='login')

def delivery(request):
    try:
        branch_id = request.session.get('branch_id')
        branch = get_object_or_404(CateringBranch, pk=branch_id)
        user = request.user
        selected_items_id = request.session.get('selected_items', [])
        selected_items = branch.caterer_food_details.filter(pk__in=selected_items_id)

        totalAmountFood, delivery_cost, gst_amount, totalAmount, advanceAmount = calculate_bill(branch, request, selected_items)

        userAddress = user.addresses.filter(is_active=True).first()
        if not userAddress:
            redirect_url = reverse('create_address_phone')
            return redirect(f"{redirect_url}?entity_type=user")

        if request.method == 'POST':
            paid = float(request.POST.get("amount"))
            note = request.POST.get("note")
            order_instance, error = create_order_and_delivery(request, user, branch, selected_items, paid, note)
            if error:
                messages.error(request, error)
            else:
                delete_order_details(request)  # Reset session data
                return redirect("success")

        context = {
            'selected_items': selected_items,
            'delivery_cost': delivery_cost,
            'totalAmountFood': totalAmountFood,
            'totalAmount': totalAmount,
            'advanceAmount': advanceAmount,
        }
        return render(request, 'delivery.html', context)

    except Http404 as e:
        traceback.print_exc()
        return HttpResponse(f"Error: {e}", status=404)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(f"Error: {e}", status=500)

def create_address_and_phone_contact(request):
    entity_type = request.GET.get('entity_type')
    if not entity_type or entity_type not in ['user', 'caterer']:
        raise Http404("Invalid entity type")

    if not request.user.is_authenticated:
        return redirect('login')

    if entity_type == 'caterer':
        branch_id = request.GET.get('branch_id')
        branch = get_object_or_404(CateringBranch, pk=branch_id)
        user = None
    else:
        user = request.user
        branch = None

    if request.method == 'POST':
        data = {
            'address': request.POST,
            'phone': request.POST
        }
        _, error = create_address_and_phone(data, entity_type, user, branch, use_serializers=False)
        if error:
            messages.error(request, error)
            # Re-render with POST data to preserve entered values
            return render(request, 'address_and_phone_form.html', {
                'address_form': AddressForm(request.POST),
                'phone_form': PhoneContactForm(request.POST),
            })
        messages.success(request, "Address and Phone Contact created successfully.")
        return redirect('success')
    else:
        return render(request, 'address_and_phone_form.html', {
            'address_form': AddressForm(),
            'phone_form': PhoneContactForm(),
        })

@login_required(login_url='login')
def catererform(request):
    existing_caterer = CateringBranch.objects.filter(user_id=request.user).first()
    if request.method == 'POST':
        form = CateringPackageForm(request.POST, request.FILES, instance=existing_caterer)
        if form.is_valid():
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']
            latitude,longitude=Location.get_coordinates(','.join([city,state,zip_code]))
            if 'image' in request.FILES:
                if existing_caterer.branches.image:
                    existing_caterer.branches.image.delete()
            form.save()
            catererForm = form.save(commit=False)
            catererForm.user_id = request.user  # Assign the current user
            catererForm.latitude=float(latitude)
            catererForm.longitude=float(longitude)
            catererForm.save()
            return redirect('manage_menu_categories')
            # Redirect to a success page
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = CateringPackageForm()

    return render(request, 'catererForm.html', {'form': form, 'user': request.user, 'caterer': existing_caterer})

def success(request):
    return render(request, 'success.html')

@login_required(login_url='login')
def catererAdmin(request):
    return render(request, 'catererAdmin.html')

@login_required(login_url='login')
def catererMenu(request):
    existing_caterer = CateringBranch.objects.filter(user_id=request.user).first()

    if request.method == 'POST':
        form = CateringPackageForm(request.POST, request.FILES, instance=existing_caterer)
        if form.is_valid():
            save_or_update_caterer_branch(request.user, form)
            return redirect('manage_menu_categories')
    else:
        form = CateringPackageForm(instance=existing_caterer)

    return render(request, 'catererForm.html', {
        'form': form,
        'user': request.user,
        'caterer': existing_caterer
    })

@login_required(login_url='login')
def catererRemove(request):
    food_list=[]
    if(request.method == 'GET'):
        item_to_remove=request.GET.get("delete")
        food_list = request.session.get('caterer_food_item', [])
        food_list.remove(item_to_remove)
        request.session['caterer_food_item'] = food_list
        
        return redirect("catererMenu")
    
@login_required(login_url='login')   
def orderDetails(request):
    sort = request.GET.get('sort', 'id')
    status_filter = request.GET.get('status')
    page_number = request.GET.get('page', 1)

    orders, page_obj = get_filtered_sorted_orders(
        user=request.user,
        sort=sort,
        status_filter=status_filter,
        page_number=page_number
    )

    if request.method == "POST":
        order_id = request.POST["id"]
        order = get_object_or_404(Order, id=order_id)
        order.status = "delivered"
        order.save()

    return render(request, 'orderDetails.html', {
        'orders': orders,
        'page_obj': page_obj,
        'sort': sort,
        'current_status': status_filter,
    })

@login_required(login_url='login')
def catererCatagory(request):
    user = get_object_or_404(User, username=request.user)
    branch = get_object_or_404(CateringBranch, user_id=user.id)
    amount = branch.starting_price

    all_categories = MenuCategory.objects.all()
    existing_details = {
        detail.menu.name: detail
        for detail in MenuCategoryDetails.objects.filter(branch=branch)
    }

    CategoryFormSet = formset_factory(MenuCategoryItemForm, extra=0)
    initial_data = [{
        'name': cat.name,
        'label': cat.get_name_display(),
        'cost': existing_details.get(cat.name).cost if existing_details.get(cat.name) else 0
    } for cat in all_categories]

    if request.method == 'POST':
        formset = CategoryFormSet(request.POST)
        if formset.is_valid():
            update_menu_category_costs(request.user, formset.cleaned_data)
            return redirect('success')
    else:
        formset = CategoryFormSet(initial=initial_data)

    return render(request, 'catererCatagory.html', {
        'formset': formset,
        'amount': amount,
    })



@login_required(login_url='login')
def foodForm(request):
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catererMenu')  # Redirect to a success page after saving
    else:
        form = FoodForm()
    return render(request, 'foodForm.html', {'form': form})


@login_required(login_url='login')
def myOrder(request):
    orders = get_user_orders(request.user)

    food_to_show = request.GET.get('show')
    if food_to_show:
        selected_items, _ = get_order_food_items(food_to_show)
        return render(request, 'myOrder.html', {
            'orders': orders,
            'selected_items': selected_items,
            'type': MenuCategory.CATEGORY_CHOICES,
        })

    return render(request, 'myOrder.html', {'orders': orders})

@login_required(login_url='login')
def dashboard(request):
    is_previous = request.GET.get('ispreviuos', 'false').lower() == 'true'
    orders_per_day, orders = get_weekly_order_stats(request.user, is_previous)
    return render(request, 'dashboard.html', {
        'orders_per_day': orders_per_day,
        'orders': orders
    })


def FullOrderDetails(request, id):
    orders = get_object_or_404(Order, id=id)
    
    # Get food items associated with this order
    food_items = OrderedFood.objects.filter(order=orders)
    
    # Get the list of food IDs directly using values_list to improve efficiency
    food_list = food_items.values_list('food_id', flat=True)
    
    # Query the Food model using the list of IDs
    selected_items = Food.objects.filter(id__in=food_list)
    
    # Get the type choices (ensure TYPE_CHOICES_ANOTHER is defined properly in your Food model)
    type_choices = MenuCategory.CATEGORY_CHOICES
    
    return render(request, 'FullOrderDetails.html', {
        'order': orders,
        'selected_items': selected_items,
        'type': type_choices,  # Pass the food type choices to the template
    })
        
        
@login_required(login_url='login')
def manage_menu_categories(request):
    if request.method == 'POST':
        form = MenuCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_category_list')  # or wherever you want to go next
    else:
        form = MenuCategoryForm()
    
    return render(request, 'menu/create_menu_category.html', {'form': form})    
    