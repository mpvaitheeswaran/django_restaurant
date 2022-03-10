
from payments.models import PackOrder
from qrmenu.models import Pack, RestaurantDetail
from . import Checksum
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def payment(request):
    order_id = Checksum.__id_generator__()
    pack_type = request.GET.get('pack_type')
    restaurant = RestaurantDetail.objects.get(user=request.user)
    bill_amount = None
    if pack_type == '1':
        bill_amount = "199"
    elif pack_type == '2':
        bill_amount = "999"
    
    pack_order = PackOrder.objects.create(order_id=order_id,
        restaurant = restaurant,
        pack_type = pack_type,
        order_amount = bill_amount)
    pack_order.save()
    param_dict = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'ORDER_ID': order_id,
        'TXN_AMOUNT': bill_amount,
        'CUST_ID': request.user.email,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'DEFAULT',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://localhost:8000/payments/response/',
        # this is the url of handlepayment function, paytm will send a POST request to the fuction associated with this CALLBACK_URL
    }
    # create new checksum (unique hashed string) using our merchant key with every paytm payment
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, settings.PAYTM_MERCHANT_KEY)
    
    context = {
        'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
        'comany_name': settings.PAYTM_COMPANY_NAME,
        'param_dict': param_dict
    }
    return render(request, 'payments/payment.html', context)


@csrf_exempt
def response(request):
    checksum = ""
    # the request.POST is coming from paytm
    form = request.POST

    response_dict = {}
    pack_order = None  # initialize the order varible with None

    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            # 'CHECKSUMHASH' is coming from paytm and we will assign it to checksum variable to verify our paymant
            checksum = form[i]

        if i == 'ORDERID':
            # we will get an order with id==ORDERID to turn isPaid=True when payment is successful
            # order = Order.objects.get(id=form[i])
            pack_order = PackOrder.objects.get(order_id = form[i])
    # we will verify the payment using our merchant key and the checksum that we are getting from Paytm request.POST
    verify = Checksum.verify_checksum(response_dict, settings.PAYTM_MERCHANT_KEY, checksum)

    if verify:
        if response_dict['RESPCODE'] == '01':
            # if the response code is 01 that means our transaction is successfull
            # after successfull payment we will make Activate the pack.
            pack_order.isPaid = True
            pack_order.save()
            pack = Pack.objects.get(restaurant = pack_order.restaurant)
            start_date = datetime.datetime.now()
            if pack_order.pack_type == '1':
                expiry_date = start_date + datetime.timedelta(days=30)
            elif pack_order.pack_type == '2':
                expiry_date = start_date + datetime.timedelta(days=365)
            else:
                expiry_date = None
            pack.pack_type = int(pack_order.pack_type)
            pack.start_date = start_date
            pack.expiry_date = expiry_date
            pack.save()

            return render(request, 'payments/payment_status.html', {'response': response_dict})
        else:
            
            return render(request, 'payments/payment_status.html', {'response': response_dict})
