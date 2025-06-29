from typing import Any
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import datetime
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from catrinmodel.models import CateringService, CateringBranch,MenuCategory, MenuCategoryDetails, Food, CatererFood, CateringPackage, Address, Order, OrderedFood, CancelledOrder, Delivery,BankDetails,PhoneContact

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(CreateUserForm,self).__init__(*args, **kwargs)
        last_user=User.objects.last() 
        current_date_string = datetime.now().strftime("%d%m%Y")
        if last_user:
            last_id = last_user.id
            self.initial['username'] = 'userid'+current_date_string+str(last_id + 1)
        else:
            self.initial['username'] = 'userid'+current_date_string+'1'

class MenuCategoryItemForm(forms.Form):
    name = forms.CharField(widget=forms.HiddenInput())
    label = forms.CharField(disabled=True, required=False)
    cost = forms.DecimalField(max_digits=10, decimal_places=2)

class CateringServiceForm(forms.ModelForm):
    class Meta:
        model = CateringService
        fields = '__all__'

class CateringBranchForm(forms.ModelForm):
    class Meta:
        model = CateringBranch
        fields = '__all__'
        
class CateringPackageForm(forms.ModelForm):
    class Meta:
        model = CateringPackage
        fields = '__all__'


class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategoryDetails
        fields = '__all__'

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'
        
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'entity_type', 'user', 'branch', 'street', 'city', 
            'state', 'zip_code', 'country', 'latitude', 'longitude', 'is_active'
        ]
    
    entity_type = forms.ChoiceField(choices=Address.ENTITY_TYPES, required=False, widget=forms.HiddenInput())  # Hide entity_type
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False, widget=forms.HiddenInput())  # Hide user
    branch = forms.ModelChoiceField(queryset=CateringBranch.objects.all(), required=False, widget=forms.HiddenInput())  # Hide branch
    street = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=20)
    zip_code = forms.CharField(max_length=20)
    country = CountryField().formfield()
    latitude = forms.DecimalField(max_digits=11, decimal_places=6, required=True, widget=forms.HiddenInput())  # Hide latitude
    longitude = forms.DecimalField(max_digits=11, decimal_places=6, required=True, widget=forms.HiddenInput())  # Hide longitude
    is_active = forms.BooleanField(initial=True)

        
class BankDetailsForm(forms.ModelForm):
    class Meta:
        model = BankDetails
        fields = '__all__'
        
class CancelledOrderForm(forms.ModelForm):
    class Meta:
        model = CancelledOrder
        fields = '__all__'
        
        
class PhoneContactForm(forms.ModelForm):
    class Meta:
        model = PhoneContact
        fields = ['entity_type', 'user', 'branch', 'phone_number', 'contact_type']

    entity_type = forms.ChoiceField(choices=PhoneContact.ENTITY_TYPES, required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    branch = forms.ModelChoiceField(queryset=CateringBranch.objects.all(), required=False)
    phone_number = PhoneNumberField(region='IN')  # Ensure phone number is valid
    contact_type = forms.CharField(max_length=50, required=False)
        
        
class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['name']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
        }



class MenuCategoryItemForm(forms.Form):
    name = forms.CharField(widget=forms.HiddenInput())
    label = forms.CharField(label='Category', required=False, disabled=True)
    cost = forms.DecimalField(label='Cost', min_value=0)