from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView,DetailView,FormView

from payments.models import PackOrder
from .forms import AccountSettingForm, EnquiryForm, RestaurantForm,MenuCategoryForm,MenuItemForm,BillingDetailForm
from .models import AccountSetting, BillingDetail, CustomerOrder, Enquiry, MenuCategory, MenuItem, OrderedMenu, Pack, RestaurantDetail, ScanCount
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model
import json
import qrcode
# from qrcode.image.styledpil import StyledPilImage
# from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
# from qrcode.image.styles.colormasks import RadialGradiantColorMask
import qrcode.image.svg
from io import BytesIO
import base64
from notifications.signals import notify
from notifications.models import Notification
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
import datetime
from qrmenu.utils import checkMenuLimit, checkScanLimit
from accounts.models import CustomUser
from .process import html_to_pdf
from django.conf import settings
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.core.files import File
from googletrans import Translator
# Create your views here.
@login_required
def select_pack(request):
    context = {}
    if not request.user.is_anonymous:
        restaurant = RestaurantDetail.objects.get(user=request.user)
        context['restaurant'] = restaurant
    return render(request,'qrmenu/select_pack.html',context)
@login_required
def activateTrial(request):
    restaurant = RestaurantDetail.objects.get(user=request.user)
    # Return back is used already used free pack.
    if restaurant.is_free_pack_used:
        return redirect('dashboard')
    restaurant.is_free_pack_used = True
    restaurant.save()
    pack = Pack.objects.get(restaurant=restaurant)
    pack.pack_type = 0
    start_date = datetime.datetime.now()
    expiry_date = start_date + datetime.timedelta(days=30)
    pack.start_date = start_date
    pack.expiry_date = expiry_date
    pack.save()
    # Send invoice to email.
    context = {
            'restaurant':restaurant,
            'item':'Free Trial',
            'paywith':'Free'
        }
    pdf = html_to_pdf('qrmenu/invoice.html',context_dict=context)
    if pdf:
        filename = 'purchase_%s.pdf' % (request.user.id)
        invoice_file = File(BytesIO(pdf.content),filename)
        restaurant.invoice_pdf = invoice_file
        restaurant.save()
        email_pdf = EmailMultiAlternatives(
            subject='Wellcome to the RestaurantQR',
            body='The Invoice for your RestaurantQR account.',
            from_email='',
            to=[request.user.email],
        )
        email_pdf.attach_alternative(restaurant.invoice_pdf.read(), "application/pdf")
        email_pdf.send()
    return redirect('dashboard')
class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        restaurant = RestaurantDetail.objects.get(user=request.user)
        context = {
             'restaurant':restaurant,
             'pack_order':{'pack_type':'2','order_amount':'200'},
             'item':'Yearly Pack',
             'paywith': 'PayTm Business'
         }
        # getting the template
        pdf = html_to_pdf('qrmenu/invoice.html',context_dict=context)
        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')

@login_required
@user_passes_test(lambda u: not u.is_superuser,redirect_field_name=None, login_url='/admin/')
def dashboard(request):
    restaurant = RestaurantDetail.objects.get(user=request.user)
    # Redirect to pack page when user not selected any package.
    if restaurant.pack.pack_type==-1:
        return redirect('qrmenu-pack')
    print(restaurant.pack.pack_type)
    menu_count = MenuItem.objects.filter(category__restaurant=restaurant).count()

    total_scan = ScanCount.objects.filter(restaurant=restaurant).count()
    context ={
        'total_menus': menu_count,
        'total_scan': total_scan,
        'pending_orders': CustomerOrder.objects.filter(restaurant=restaurant,status='pending').count()
    }
    return render(request,'qrmenu/dashboard.html',context)

class RestaurantView(UserPassesTestMixin,View):
    # Redirect when user was superuser.
    login_url='/admin/'
    redirect_field_name = None 
    def test_func(self):
        return not self.request.user.is_superuser
    def handle_no_permission(self):
        return redirect(self.login_url)
    
    template_name = 'qrmenu/restaurant.html'
    form_class = RestaurantForm
    context = {}
    def get(self,request):
        try:
            restaurant = RestaurantDetail.objects.get(user=request.user)
            form = self.form_class(instance=restaurant)
        except RestaurantDetail.DoesNotExist:
            form = self.form_class()
        self.context['form'] = form
        return render(request,self.template_name,self.context)
    def post(self,request):
        try:
            restaurant = RestaurantDetail.objects.get(user=request.user)
            form = self.form_class(request.POST,request.FILES,instance=restaurant)
        except RestaurantDetail.DoesNotExist:
            form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('restaurant')
        self.context['form'] = form
        return render(request,self.template_name,self.context)

class MenuView(UserPassesTestMixin,TemplateView):
    # Redirect when user was superuser.
    login_url='/admin/'
    redirect_field_name = None 
    def test_func(self):
        return not self.request.user.is_superuser
    def handle_no_permission(self):
        return redirect(self.login_url)

    template_name = 'qrmenu/menu.html'
    form_menucategory = MenuCategoryForm
    form_menuitem = MenuItemForm

    def get_context_data(self, **kwargs):
        restaurant = RestaurantDetail.objects.get(user=self.request.user)
        account_setting = AccountSetting.objects.get(restaurant=restaurant)
        context = super().get_context_data(**kwargs)
        context['form_menucategory'] = self.form_menucategory()
        context['form_menuitem'] = self.form_menuitem()
        context['menu_category'] = MenuCategory.objects.filter(restaurant=restaurant)
        context['items'] = MenuItem.objects.all()
        context['currency'] = account_setting.currency_model
        return context

class NotificationView(UserPassesTestMixin,TemplateView):
    # Redirect when user was superuser.
    login_url='/admin/'
    redirect_field_name = None 
    def test_func(self):
        return not self.request.user.is_superuser
    def handle_no_permission(self):
        return redirect(self.login_url)

    template_name = 'qrmenu/notifications.html'
    unread_notifications = None
    def get(self, request, *args, **kwargs):
        self.unread_notifications = self.request.user.notifications.unread()
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_notifications'] = self.unread_notifications
        return context

class OrdersView(UserPassesTestMixin,TemplateView):
    # Redirect when user was superuser.
    login_url='/admin/'
    redirect_field_name = None 
    def test_func(self):
        return not self.request.user.is_superuser
    def handle_no_permission(self):
        return redirect(self.login_url)

    template_name = 'qrmenu/orders.html'
    notifications = None
    def get(self, request, *args, **kwargs):
        self.notifications = self.request.user.notifications.all()
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        restaurant = RestaurantDetail.objects.get(user=self.request.user)
        account_setting = AccountSetting.objects.get(restaurant=restaurant)
        context = super().get_context_data(**kwargs)
        context['notifications'] = self.notifications
        context['orders'] = CustomerOrder.objects.filter(restaurant=restaurant)
        context['currency'] = account_setting.currency_model
        return context
def aproveOrder(request):
    if request.method=='POST' and request.is_ajax():
        responce_data = {}
        order_id = request.POST.get('id')
        order = CustomerOrder.objects.get(id=order_id)
        order.status = 'success'
        order.success = True
        order.save()
        return HttpResponse(json.dumps(responce_data), content_type="application/json")
def deleteOrder(request):
    if request.method=='POST' and request.is_ajax():
        responce_data = {}
        order_id = request.POST.get('id')
        order = CustomerOrder.objects.get(id=order_id)
        order.delete()
        return HttpResponse(json.dumps(responce_data), content_type="application/json")
class BillTemplate(DetailView):
    model = CustomerOrder
    template_name = 'qrmenu/bill_template.html'
    context_object_name = 'order'
@login_required
def delete_old_orders(request):
    if request.is_ajax():
        responce_data = {}
        restaurant = RestaurantDetail.objects.get(user=request.user)
        d = timezone.now() - datetime.timedelta(hours=24)
        #get expired orders
        orders = CustomerOrder.objects.filter(restaurant=restaurant,timestamp__lt=d)
        #delete them
        orders.delete()
        # Change pack type after user pack expired.
        pack = Pack.objects.get(restaurant=restaurant)
        if pack.expiry_date < timezone.now().date():
            pack.pack_type = -1
            pack.start_date = None
            pack.expiry_date = None
            pack.save()
        return HttpResponse(json.dumps(responce_data), content_type="application/json")

class MembershipView(TemplateView):
    template_name = 'qrmenu/membership.html'

@login_required
@user_passes_test(lambda u: not u.is_superuser,redirect_field_name=None, login_url='/admin/')
def qrBuilder(request):
    context = {}
    host_name = request.META['HTTP_HOST']
    restaurant = RestaurantDetail.objects.get(user=request.user)
    url = f'http://{host_name}/restaurant/{restaurant.unique_id}/{restaurant.name}'
    # factory = qrcode.image.svg.SvgImage
    # img = qrcode.make(url,image_factory=factory,box_size=20)
    # stream = BytesIO()
    # img.save(stream)
    # context['svg'] = stream.getvalue().decode()

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L,
        version=1,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    # img = qr.make_image(image_factory=StyledPilImage,module_drawer=RoundedModuleDrawer())
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer,'PNG')
    img_str = base64.b64encode(buffer.getvalue())
    img_base64 = bytes("data:image/png;base64,", encoding='utf-8') + img_str
    context['img_str'] = img_base64.decode('utf-8')
    context['restaurant'] = restaurant
    return render(request,'qrmenu/qrbuilder.html',context)

class TransactionView(UserPassesTestMixin,TemplateView):
    # Redirect when user was superuser.
    login_url='/admin/'
    redirect_field_name = None 
    def test_func(self):
        return not self.request.user.is_superuser
    def handle_no_permission(self):
        return redirect(self.login_url)

    template_name = 'qrmenu/transactions.html'

    def get_context_data(self, **kwargs):
        restaurant = RestaurantDetail.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['pack_orders'] = PackOrder.objects.filter(restaurant=restaurant)
        context['restaurant'] = restaurant
        return context

class AccountSettingsView(UserPassesTestMixin,View):
    # Redirect when user was superuser.
    login_url='/admin/'
    redirect_field_name = None 
    def test_func(self):
        return not self.request.user.is_superuser
    def handle_no_permission(self):
        return redirect(self.login_url)

    template_name = 'qrmenu/accountsettings.html'
    form_class1 = BillingDetailForm
    form_class2 = AccountSettingForm
    context = {}
    def get(self,request):
        restaurant = RestaurantDetail.objects.get(user=request.user)
        try:
            billing_detail = BillingDetail.objects.get(restaurant=restaurant)
            form = self.form_class1(instance=billing_detail)
        except BillingDetail.DoesNotExist:
            form = self.form_class1()
        try:
            account_setting = AccountSetting.objects.get(restaurant=restaurant)
            accountsettingform = self.form_class2(instance=account_setting)
        except AccountSetting.DoesNotExist:
            accountsettingform = self.form_class2()
        passwordform = PasswordChangeForm(request.user)
        self.context['form'] = form
        self.context['accountsettingform'] = accountsettingform
        self.context['passwordform'] = passwordform
        self.context['useremail'] = request.user.email
        return render(request,self.template_name,self.context)
    def post(self,request):
        try:
            restaurant = RestaurantDetail.objects.get(user=request.user)
            billing_detail = BillingDetail.objects.get(restaurant=restaurant)
            form = self.form_class1(request.POST,instance=billing_detail)
        except BillingDetail.DoesNotExist:
            form = self.form_class1(request.POST)
       
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('accountsettings')
        self.context['form'] = form
        return render(request,self.template_name,self.context)

class SupportView(UserPassesTestMixin,FormView):
    # Redirect when user was superuser.
    login_url='/admin/'
    redirect_field_name = None 
    def test_func(self):
        return not self.request.user.is_superuser
    def handle_no_permission(self):
        return redirect(self.login_url)

    template_name = 'qrmenu/support.html'
    form_class = EnquiryForm
    success_url = reverse_lazy('support')

    def get_context_data(self, **kwargs):
        restaurant = RestaurantDetail.objects.get(user=self.request.user)
        enquiries = Enquiry.objects.filter(restaurant=restaurant)
        context = super().get_context_data(**kwargs)
        context['enquiries'] = enquiries
        return context
    def form_valid(self, form):
        restaurant = RestaurantDetail.objects.get(user=self.request.user)
        enquiry = form.save(commit=False)
        enquiry.restaurant = restaurant
        enquiry.save()
        admin = CustomUser.objects.filter(is_superuser=True)
        notify.send(enquiry, 
            recipient=admin, 
            verb='Query',
            description=f'{enquiry.title}',
            level='success')
        # Send mail to the user after enquiry recived.
        email = EmailMessage(
            subject='Enquiry Recieved',
            body='Thankyou for your enquiry. we will response back the problem soon.',
            from_email='',
            to=[self.request.user.email],
        )
        email.send()
        return super().form_valid(form)

def changePassword(request):
    if request.method == 'POST':
        passwordform = PasswordChangeForm(request.user,request.POST)
        restaurant = RestaurantDetail.objects.get(user=request.user)
        try:
            account_setting = AccountSetting.objects.get(restaurant=restaurant)
            settingsform = AccountSettingForm(request.POST,instance=account_setting)
        except AccountSetting.DoesNotExist:
            settingsform = AccountSettingForm(request.POST)
        
        if settingsform.is_valid():
            settings = settingsform.save(commit=False)
            settings.restaurant = restaurant
            settings.save()
        if passwordform.is_valid():
            user = passwordform.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Password successfuly changed!')
        else: 
            if passwordform.data['old_password']:
                messages.error(request,'Wrong Password!')
        return redirect('accountsettings')

# for customers
class CustomerView(TemplateView):
    template_name = 'qrmenu/customer_view/customer_menu.html'
    def get(self, request, *args, **kwargs):
        unique_id = self.kwargs['unique_id']
        restaurant = RestaurantDetail.objects.get(unique_id=unique_id)
        pack = Pack.objects.get(restaurant=restaurant)
        # Change the template when user plan expired or out of scan limit.
        if not checkScanLimit(pack) or pack.pack_type==-1:
            self.template_name = 'qrmenu/customer_view/outofscans.html'
        return super().get(request, *args, **kwargs)
    def render_to_response(self, context, **response_kwargs):
        from django.utils import translation
        unique_id = self.kwargs['unique_id']
        restaurant = RestaurantDetail.objects.get(unique_id=unique_id)
        account_setting = AccountSetting.objects.get(restaurant=restaurant)
        user_language = account_setting.menu_language
        translation.activate(user_language)
        response = super().render_to_response(context, **response_kwargs)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
        return response
    def get_context_data(self, **kwargs):
        def get_client_ip(request):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip
        unique_id = self.kwargs['unique_id']
        restaurant = RestaurantDetail.objects.get(unique_id=unique_id)
        account_setting = AccountSetting.objects.get(restaurant=restaurant)
        categories = MenuCategory.objects.filter(restaurant=restaurant)
        ip = get_client_ip(self.request)
        scan_count = ScanCount(restaurant=restaurant,ip=ip)
        result = ScanCount.objects.filter(ip=ip)
        if len(result)>=1:
            # print('User exsist')
            pass
        else:
            scan_count.save()
            # print('user ip Saved')
        
        context = super().get_context_data(**kwargs)
        context['restaurant'] = restaurant
        context['categories'] = categories
        context['currency'] = account_setting.currency_model
        return context
# for customers
class MenuItemView(TemplateView):
    template_name = 'qrmenu/customer_view/customer_menu_item.html'
    def get(self, request, *args, **kwargs):
        unique_id = self.kwargs['unique_id']
        restaurant = RestaurantDetail.objects.get(unique_id=unique_id)
        pack = Pack.objects.get(restaurant=restaurant)
        # Change the template when user plan expired or out of scan limit.
        if not checkScanLimit(pack) or pack.pack_type==-1:
            self.template_name = 'qrmenu/customer_view/outofscans.html'
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        unique_id = self.kwargs['unique_id']
        
        category_id = self.kwargs['category_id']
        restaurant = RestaurantDetail.objects.get(unique_id=unique_id)
        account_setting = AccountSetting.objects.get(restaurant=restaurant)
        categories = MenuCategory.objects.filter(restaurant=restaurant)
        category = MenuCategory.objects.get(pk=category_id)
        menu_items = MenuItem.objects.filter(category=category)
        menus=[]
        for category1 in MenuCategory.objects.filter(restaurant=restaurant):
            for menu in MenuItem.objects.filter(category=category1):
                menus.append(menu)
    
        context = super().get_context_data(**kwargs)
        context['restaurant'] = restaurant
        context['categories'] = categories
        context['category_name'] = category.name
        context['menu_items'] = menu_items
        context['menus']=menus
        context['currency'] = account_setting.currency_model
        return context
def placeOrder(request):
    response_data={}
    if request.method=='POST' and request.is_ajax():
        customer_name = request.POST.get('cus_name')
        table_no = request.POST.get('table_no')
        ordered_menu_data = json.loads(request.POST.get('ordered_menus'))
        total_price = float(request.POST.get('total_price'))
        unique_id = request.POST.get('unique_id')
        restaurant = RestaurantDetail.objects.get(unique_id=unique_id)
        user = restaurant.user
        cus_order = CustomerOrder.objects.create(restaurant=restaurant,customer_name=customer_name,
            table_no=table_no,
            total_price=total_price,
        )
        if restaurant.pickup:
            dinein_or_pickup = request.POST.get('dinein_or_pickup')
            cus_order.order_type = dinein_or_pickup
        cus_order.save()
        for menu in ordered_menu_data:
            menu_item = MenuItem.objects.get(id=ordered_menu_data[menu]['id'])
            qt = ordered_menu_data[menu]['qt']
            if not qt == 0:
                order_menu = OrderedMenu.objects.create(menu=menu_item,quantity=qt)
                cus_order.ordered_menu.add(order_menu)
        if request.POST.get('dinein_or_pickup') == 'pickup':
            notify.send(cus_order, recipient=user, verb='Order',description=f'{customer_name} Placing Pickup Order',level='success')
        else:
            notify.send(cus_order, recipient=user, verb='Order',description=f'{customer_name} Placing Order from table {table_no}',level='success')
        return JsonResponse(response_data)
def callWaiter(request):
    response_data = {}
    if request.method=='POST' and request.is_ajax():
        unique_id = request.POST.get('unique_id')
        table_no = request.POST.get('table_no')
        restaurant = RestaurantDetail.objects.get(unique_id=unique_id)
        user = restaurant.user
        notify.send(user, recipient=user, verb='Calling Waiter',description=f'The customer calling from table {table_no}')
        return JsonResponse(response_data)

#Ajax request methods
@csrf_protect
def addCategory(request):
    if request.method=='POST' and request.is_ajax():
        name = request.POST.get('name')
        translator = Translator()
        responce_data ={}
        #Create a MenuCategory object.
        restaurant = RestaurantDetail.objects.get(user=request.user)
        category = MenuCategory(restaurant=restaurant,name=name)
        # For Translation.
        category.name_ta = translator.translate(name,dest='ta',src='en').text
        category.name_ar = translator.translate(name,dest='ar',src='en').text
        category.save()
        responce_data['id'] = category.pk
        responce_data['name'] = category.name
        return HttpResponse(json.dumps(responce_data), content_type="application/json")

@csrf_protect
def editCategory(request):
    if request.method=='POST' and request.is_ajax():
        id = request.POST.get('id')
        new_name = request.POST.get('new_name')
        translator = Translator()
        responce_data ={}
        category = MenuCategory.objects.get(pk=id)
        category.name = new_name
        category.name_ta = translator.translate(new_name,dest='ta',src='en').text
        category.name_ar = translator.translate(new_name,dest='ar',src='en').text
        category.save()
        responce_data['name'] = category.name
        return HttpResponse(json.dumps(responce_data), content_type="application/json")

@csrf_protect
def reorderCategory(request):
    if request.method=='POST' and request.is_ajax():
        ids = request.POST.getlist('ids[]')
        responce_data ={}
        for idx, id in enumerate(ids,start=1):
            category = MenuCategory.objects.get(pk=id)
            category.order = idx
            category.save()
        return HttpResponse(json.dumps(responce_data), content_type="application/json")

@csrf_protect
def addItem(request):
    restaurant = RestaurantDetail.objects.get(user=request.user)
    pack = Pack.objects.get(restaurant=restaurant)
    if request.method=='POST' and request.is_ajax():
        responce_data ={}
        translator = Translator()
        category_id = int(request.POST.get('id'))
        display = request.POST.get('display')
        if display:
            display = True
        else:
            display = False
        form = MenuItemForm(request.POST,request.FILES)
        if pack.pack_type==-1:
            # if user didn't select the pack.
            responce_data['no_pack'] = True
            return HttpResponse(json.dumps(responce_data), content_type="application/json")
        if checkMenuLimit(pack):
            if form.is_valid():
                category = MenuCategory.objects.get(pk=category_id)
                item = form.save(commit=False)
                item.category = category
                item.display = display
                item.name_ta = translator.translate(item.name,dest='ta',src='en').text
                item.name_ar = translator.translate(item.name,dest='ar',src='en').text
                item.save()
                responce_data['error'] = False
                responce_data['id'] = item.id
                responce_data['name'] = item.name
                responce_data['price'] = item.price
                responce_data['desc'] = item.desc
                responce_data['img'] = item.img.url
                responce_data['food_type'] = item.food_type
                responce_data['display'] = item.display
                # for available time blank issue.
                if item.start_time and item.end_time:
                    responce_data['start_time'] = item.start_time.strftime("%H:%M")
                    responce_data['end_time'] = item.end_time.strftime("%H:%M")
                return HttpResponse(json.dumps(responce_data), content_type="application/json")
            # If error.
            else:
                responce_data['error'] = True
                responce_data['errors'] = form.errors
                return HttpResponse(json.dumps(responce_data), content_type="application/json")
        else:
            # Can't add menus.
            responce_data['out_of_menus'] = True
            return HttpResponse(json.dumps(responce_data), content_type="application/json")

@csrf_protect
def updateItem(request):
    if request.method=='POST' and request.is_ajax():
        responce_data ={}
        translator = Translator()
        item_id = int(request.POST.get('id'))
        item_instance = MenuItem.objects.get(pk=item_id)
        display = request.POST.get('display')
        if display:
            display = True
        else:
            display = False
        form = MenuItemForm(request.POST,request.FILES,instance=item_instance)
        if form.is_valid():
            item = form.save(commit=False)
            item.display = display
            item.name_ta = translator.translate(item.name,dest='ta',src='en').text
            item.name_ar = translator.translate(item.name,dest='ar',src='en').text
            item.save()
            print('Form valid')
            responce_data['error'] = False
            responce_data['id'] = item.id
            responce_data['name'] = item.name
            responce_data['price'] = item.price
            responce_data['desc'] = item.desc
            responce_data['img'] = item.img.url
            responce_data['food_type'] = item.food_type
            responce_data['display'] = item.display
            return HttpResponse(json.dumps(responce_data), content_type="application/json")
        # If error.
        else:
            responce_data['error'] = True
            responce_data['errors'] = form.errors
            return HttpResponse(json.dumps(responce_data), content_type="application/json")

@csrf_protect
def deleteCategory(request):
    if request.method=='POST' and request.is_ajax():
        category_id = request.POST.get('id')
        category = MenuCategory.objects.get(pk=category_id)
        category.delete()
        responce_data ={}
        return HttpResponse(json.dumps(responce_data), content_type="application/json")

@csrf_protect
def deleteItem(request):
    if request.method=='POST' and request.is_ajax():
        item_id = request.POST.get('id')
        item = MenuItem.objects.get(pk=item_id)
        item.delete()
        responce_data ={}
        return HttpResponse(json.dumps(responce_data), content_type="application/json")

# Notifications
def readNotification(request):
    if request.is_ajax():
        responce_data ={}
        id = request.GET.get('id')
        notification = Notification.objects.get(id=id)
        notification.mark_as_read()
        return HttpResponse(json.dumps(responce_data), content_type="application/json")