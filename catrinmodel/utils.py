from django.core.exceptions import ValidationError
#from catrinmodel.models import CateringService, CateringBranch, Food, CatererFood, MenuCategoryDetails, Address, Order, OrderedFood, CancelledItems, Delivery

def validate_exclusive_relationships(instance):
    """
    Ensures only one of user or caterer is set based on entity_type.

    Args:
        instance: The model instance being validated.

    Raises:
        ValidationError: If validation fails.
    """
    if instance.entity_type == 'user' and not instance.user:
        raise ValidationError("entity_type is 'user', but no user is linked.")
    elif instance.entity_type == 'caterer' and not instance.branch:
        raise ValidationError("entity_type is 'caterer', but no caterer is linked.")
    elif not instance.user and not instance.branch:
        raise ValidationError("Either user or caterer must be specified.")
    elif instance.user and instance.branch:
        raise ValidationError("Only one entity can be linked at a time (user or caterer).")
    
def make_all_active_address_false(instance):
    instance.user.addresses.exclude(id=instance.id).update(is_active=False)

def make_all_active_Bank_false(instance,entity):
    entity.bank_details.exclude(id=instance.id).update(is_active=False)
    
def check_valid_food(instance):
    if instance.food not in [bfood.food for bfood in instance.order.branch.caterer_food_details.all()]:
        raise ValidationError("food is not in the list of caterer_food")
    