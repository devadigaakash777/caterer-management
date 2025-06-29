#########     Location Method #################
from math import radians, cos, sin, sqrt, atan2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

#########    Email Method  ########################
import secrets
import string


############## Bill Method ##################
from catrinmodel.models import CateringService, CateringBranch, Food, CatererFood, MenuCategoryDetails, Address, Order, OrderedFood, CancelledOrder, Delivery
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404
from datetime import datetime
from decimal import Decimal

class Location:
    def __init__(self):
        pass
    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        r = 6371  # Radius of Earth in kilometers. Use 3956 for miles.
        return Decimal(r * c)
    
    
    @staticmethod   
    def get_coordinates(address):
        url = 'https://nominatim.openstreetmap.org/search'
        params = {
            'q': address,
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'YourAppName/1.0'
        }
        response = requests.get(url, params=params, headers=headers)

    # Check the response status code
        if response.status_code == 200:
            try:
                response_json = response.json()
                if response_json:
                    latitude = response_json[0]['lat']
                    longitude = response_json[0]['lon']
                    return latitude, longitude
                else:
                    return None, None
            except ValueError:
                print("Error decoding JSON:", response.text)
                return None, None
        else:
            print(f"Error fetching data: {response.status_code} - {response.text}")
            return None, None
        
        
class Cat_Email:
    def __init__(self) -> None:
        pass
    @staticmethod
    def generate_verification_token():
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(64))
    
class Cat_Bill:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_category_counts(selected_items):
        category_counts = selected_items.values('menu_catagory').annotate(count=Count('menu_catagory'))
        return {item['menu_catagory']: item['count'] for item in category_counts}

    @staticmethod
    def totalAmountForFood(selected_items):
        veg_total = 0
        non_veg_total = 0
        both_total = 0

        for item in selected_items:
            extra_cost=item.extra_cost
            if item.food.type_food == "veg":
                veg_total += extra_cost
            elif item.food.type_food == "non-veg":
                non_veg_total += extra_cost
            elif item.food.type_food == "both":
                both_total += extra_cost

        return (veg_total, non_veg_total, both_total)

    @staticmethod
    def calc(request,vegfixedcost,nonvegfixedcost,bothfixedcost):
        totalVegMember=int(request.session.get('functionVegMember') or 0)
        totalNonVegMember=int(request.session.get('functionNonMember') or 0)
        totalMember=totalVegMember+totalNonVegMember
        totalVegAmount=totalVegMember*float(vegfixedcost)
        totalNonVegAmount=totalNonVegMember*float(nonvegfixedcost)
        totalBothAmount=totalMember*float(bothfixedcost)

        return totalVegAmount+totalNonVegAmount+totalBothAmount


    def getTotalAmount(self,request,selected_items):
        vegfixedcost,nonvegfixedcost,bothvegfixedcost=self.totalAmountForFood(selected_items)
        return self.calc(request,vegfixedcost,nonvegfixedcost,bothvegfixedcost) 

    @staticmethod
    def dayInc(catererId,date):
        day=0
        night=0
        daymsg="day avilable"
        nightmsg="night avilable"
        Caterer=get_object_or_404(CateringBranch,id=catererId)
        orders=Order.objects.filter(delivery_date=date,caterer_id=catererId)
        for order in orders:
            if Cat_Bill.time_string_to_float(order.delivery_time)<12:
                day+=1
            else:
                night+=1
        if day == Caterer.max_order_day:
            daymsg="day not avilable"
        if night == Caterer.max_order_night:
            nightmsg="night not avilable"
        return (daymsg,nightmsg)

    @staticmethod
    def time_string_to_float(time_str):
        # Convert time string to datetime.time object
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        
        # Convert time object to float
        total_hours = time_obj.hour + time_obj.minute / 60
        return total_hours