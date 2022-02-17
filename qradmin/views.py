import django
from django.shortcuts import render
from qrmenu.models import Enquiry, RestaurantDetail,Pack
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
import json
from django.http.response import HttpResponse
# Create your views here.

@user_passes_test(lambda u: u.is_superuser,redirect_field_name=None)
def admin_dashboard(request):
    total_users = RestaurantDetail.objects.filter(~Q(user__is_superuser=True)).count()
    active_users = Pack.objects.filter(pack_type__gt = 0).count()
    inactive_users = Pack.objects.filter(pack_type = 0).count()
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
    enquiries = Enquiry.objects.filter(~Q(restaurant__user__is_superuser=True))
    context = {
        'enquiries':enquiries
    }
    return render(request,'qradmin/enquiry.html',context)

def changePack(request):
    responce_data ={}
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('user_id')
        pack_type = int(request.POST.get('pack_type'))
        restaurant = RestaurantDetail.objects.get(pk=user_id)
        pack = Pack.objects.get(restaurant=restaurant)
        pack.pack_type = pack_type
        pack.save()

        return HttpResponse(json.dumps(responce_data), content_type="application/json")

def changeStatus(request):
    responce_data ={}
    if request.method == 'POST' and request.is_ajax():
        enquiry_id = request.POST.get('enquiry_id')
        status = request.POST.get('status')
        print(status)
        enquiry = Enquiry.objects.get(pk=enquiry_id)
        enquiry.status = status
        enquiry.save()

        return HttpResponse(json.dumps(responce_data), content_type="application/json")