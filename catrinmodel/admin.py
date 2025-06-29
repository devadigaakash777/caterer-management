from django.contrib import admin
from catrinmodel.models import CateringService, CateringBranch, Food, CatererFood, MenuCategoryDetails, Address, Order, OrderedFood, CancelledOrder, Delivery, MenuCategory

class CateringServiceAdmin(admin.ModelAdmin):
    list_display = ('caterer_name', 'description', 'image', 'gstin_number', 'caterer_id')
    
admin.site.register(CateringService, CateringServiceAdmin)

class CateringBranchAdmin(admin.ModelAdmin):
    list_display = ('branch_id', 'branch_name', 'is_active')
    
admin.site.register(CateringBranch, CateringBranchAdmin)

class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class MenuCategoryDetailsAdmin(admin.ModelAdmin):
    list_display = ('branch', 'menu', 'cost')  # 'menu' is the ForeignKey field here
    list_filter = ('branch', 'menu')  # Use 'menu' to filter by MenuCategory
    search_fields = ('branch__name', 'menu__name')  # Searching within 'menu' (which is a ForeignKey)
    ordering = ('branch', 'menu')  # Sorting by 'branch' and 'menu'

class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_food', 'menu_category', 'food_image')
    list_filter = ('type_food', 'menu_category')
    search_fields = ('name', 'menu_category__name')
    ordering = ('name',)

    def food_image_preview(self, obj):
        if obj.food_image:
            return f'<img src="{obj.food_image.url}" width="50" height="50" />'
        return "No Image"
    food_image_preview.allow_tags = True
    food_image_preview.short_description = 'Image Preview'

    list_display += ('food_image_preview',)

admin.site.register(MenuCategory, MenuCategoryAdmin)
admin.site.register(MenuCategoryDetails, MenuCategoryDetailsAdmin)
admin.site.register(Food, FoodAdmin)  



class AddressAdmin(admin.ModelAdmin):
    list_display = ('entity_type', 'street', 'city', 'state', 'zip_code', 'country', 'latitude', 'longitude', 'is_active', 'is_exist')
    
admin.site.register(Address, AddressAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'branch', 'ordered_time', 'function_name', 'food_amount', 'gstin', 'total_price', 'total_member_veg', 'total_member_nonveg', 'advance_paid', 'status', 'note')
    
admin.site.register(Order, OrderAdmin)

class OrderedFoodAdmin(admin.ModelAdmin):
    list_display = ('order', 'food')
    
admin.site.register(OrderedFood, OrderedFoodAdmin)

class CancelledOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'reason')
    
admin.site.register(CancelledOrder, CancelledOrderAdmin)

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery_date', 'delivery_time', 'delivery_charge', 'period', 'delivery_note', 'address')
    
admin.site.register(Delivery, DeliveryAdmin)
