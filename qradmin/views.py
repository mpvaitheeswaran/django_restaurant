from datetime import datetime
import django
from django.shortcuts import render
from payments.models import PackOrder
from qrmenu.models import Enquiry, RestaurantDetail,Pack
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
import json
from django.http.response import HttpResponse
from notifications.signals import notify
from notifications.models import Notification
from django.template.loader import render_to_string
from django.http import JsonResponse
from accounts.models import CustomUser
# Create your views here.

@user_passes_test(lambda u: u.is_superuser,redirect_field_name=None)
def admin_dashboard(request):
    total_users = RestaurantDetail.objects.filter(~Q(user__is_superuser=True)).count()
    active_users = Pack.objects.filter(pack_type__gt = 0).count()
    inactive_users = Pack.objects.filter(pack_type = 0).count()
    users = RestaurantDetail.objects.filter(~Q(user__is_superuser=True))[:10]
    context = {
        'total_users':total_users,
        'active_users':active_users,
        'inactive_users':inactive_users,
        'users':users
    }
    return render(request,'qradmin/dashboard.html',context)

@user_passes_test(lambda u: u.is_superuser,redirect_field_name=None)
def accounts(request):
    context = {}
    url_parameter = request.GET.get("q")
    url_parameter_str = str(request.GET.get("q"))
    # url_parameter_date = request.GET.get("date")
    
    if url_parameter:
        # For searching packs.
        if url_parameter_str.lower() in 'free pack':
            url_parameter = '0'
        elif url_parameter_str.lower() in 'monthly pack':
            url_parameter = '1'
        elif url_parameter_str.lower() in 'yearly pack':
            url_parameter = '2'
            
        users = RestaurantDetail.objects.filter(Q(user__email__icontains=url_parameter)|
            Q(name__icontains=url_parameter)|
             Q(pack__pack_type__icontains=url_parameter)|
            Q(accountsetting__phone__contains=url_parameter))
        
    else:
        users = RestaurantDetail.objects.filter(~Q(user__is_superuser=True))
    if request.is_ajax():
        html = render_to_string(
            template_name="qradmin/user_list.html", 
            context={"users": users}
        )

        data_dict = {"user_list": html}

        return JsonResponse(data=data_dict, safe=False)

    context['users'] = users
    return render(request,'qradmin/accounts.html',context)

@user_passes_test(lambda u: u.is_superuser,redirect_field_name=None)
def enquiry(request):
    context = {}
    url_parameter = request.GET.get("q")
    url_parameter_date = request.GET.get("date")
    print(url_parameter_date)
    if url_parameter or url_parameter_date:
        if url_parameter and url_parameter_date:
            enquiries = Enquiry.objects.filter(Q(date__date=url_parameter_date)).filter(
                Q(restaurant__name__icontains=url_parameter)|
                Q(restaurant__user__email__icontains=url_parameter)|
                Q(restaurant__id__icontains=url_parameter)|
                Q(status__icontains=url_parameter))
        elif url_parameter_date:
            enquiries = Enquiry.objects.filter(Q(date__date=url_parameter_date))
            print(enquiries)
        elif url_parameter:
            enquiries = Enquiry.objects.filter(Q(restaurant__name__icontains=url_parameter)|
                Q(restaurant__user__email__icontains=url_parameter)|
                Q(restaurant__id__icontains=url_parameter)|
                Q(status__icontains=url_parameter))
    else:
        enquiries = Enquiry.objects.filter(~Q(restaurant__user__is_superuser=True))
    if request.is_ajax():
        html = render_to_string(
            template_name="qradmin/enquiry_list.html", 
            context={"enquiries": enquiries}
        )

        data_dict = {"enquiry_list": html}

        return JsonResponse(data=data_dict, safe=False)

    context['enquiries'] = enquiries
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
        enquiry = Enquiry.objects.get(pk=enquiry_id)
        enquiry.status = status
        enquiry.save()

        return HttpResponse(json.dumps(responce_data), content_type="application/json")

def deleteUser(request):
    responce_data ={}
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('user_id')
        user = CustomUser.objects.get(pk=user_id)
        user.delete()
        
        return HttpResponse(json.dumps(responce_data), content_type="application/json")
    
def getOrders(request):
    responce_data ={}
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('user_id')
        restaurant = RestaurantDetail.objects.get(pk=user_id)
        pack_orders = PackOrder.objects.filter(restaurant=restaurant)
        html_modal = render_to_string(
            template_name='qradmin/user_invoice_list_modal.html',
            context={'orders':pack_orders,'restaurant':restaurant}
        )   
        responce_data['modal'] = html_modal 
        return HttpResponse(json.dumps(responce_data), content_type="application/json")
