from django.shortcuts import render
from qrmenu.models import RestaurantDetail
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

@user_passes_test(lambda u: u.is_superuser,redirect_field_name=None)
def admin_dashboard(request):
    total_users = RestaurantDetail.objects.filter(~Q(user__is_superuser=True)).count()
    active_users = RestaurantDetail.objects.filter(~Q(user__is_superuser=True) & Q(is_packactive=True)).count()
    inactive_users = RestaurantDetail.objects.filter(~Q(user__is_superuser=True) & ~Q(is_packactive=True)).count()
    context = {
        'total_users':total_users,
        'active_users':active_users,
        'inactive_users':inactive_users,
    }
    return render(request,'qradmin/dashboard.html',context)

@user_passes_test(lambda u: u.is_superuser,redirect_field_name=None)
def accounts(request):
    context = {
        'users':RestaurantDetail.objects.filter(~Q(user__is_superuser=True))
    }
    return render(request,'qradmin/accounts.html',context)

@user_passes_test(lambda u: u.is_superuser,redirect_field_name=None)
def enquiry(request):
    return render(request,'qradmin/enquiry.html')