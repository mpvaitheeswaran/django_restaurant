from .models import RestaurantDetail,MenuCategory,MenuItem

def add_variable_to_context(request):
    # restaurant = RestaurantDetail.objects.get(user=request.user)
    context = {
        # 'restaurant':restaurant,
        # 'category_list': MenuCategory.objects.filter(restaurant=restaurant),
        # 'menu_list': MenuItem.objects.all(),
    }
    return context