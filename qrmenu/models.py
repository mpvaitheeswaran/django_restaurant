import datetime
from struct import pack
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.utils.crypto import get_random_string
from currencies.models import Currency

# Create your models here.
class RestaurantDetail(models.Model):
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    unique_id = models.CharField(max_length=15,null=True,blank=True,unique=True,editable=False)
    name = models.CharField(max_length=100,null=True)
    gstin = models.CharField(max_length=15,blank=True,null=True)
    desc = models.TextField(null=True)
    location = models.CharField(max_length=100,null=True)
    image = models.ImageField(upload_to='restaurant_image',default='default/default.png',null=True)
    logo = models.ImageField(upload_to='restaurant_logo',default='default/default.png',null=True)
    menu_count = models.IntegerField(default=0,null=True)
    allowCalltoWaiter = models.BooleanField(default=True,blank=True,choices=BOOL_CHOICES)
    allowCustomerOrder = models.BooleanField(default=False,blank=True,choices=BOOL_CHOICES)
    pickup = models.BooleanField(default=False,blank=True,choices=BOOL_CHOICES)
    total_tables = models.PositiveIntegerField(default=5,blank=True)
    invoice_pdf = models.FileField(upload_to='invoice_pdfs',null=True,blank=True)
    def __str__(self) -> str:
        return f'{self.name}'
# Signal
def unique_id_generator(sender,instance,*args,**kwargs):
    if not instance.unique_id:
        id = get_random_string(10)
        while RestaurantDetail.objects.filter(unique_id=id).exists():
            id = get_random_string(10)
        instance.unique_id = id
def create_billing_detail(sender,instance,created,*args,**kwargs):
    if created:
        BillingDetail.objects.create(restaurant=instance)
        AccountSetting.objects.create(restaurant=instance)
        Pack.objects.create(restaurant=instance)
pre_save.connect(unique_id_generator, sender=RestaurantDetail)
post_save.connect(create_billing_detail,sender=RestaurantDetail)

class Pack(models.Model):
    restaurant = models.OneToOneField(RestaurantDetail,on_delete=models.CASCADE,null=True)
    total_menus = models.PositiveIntegerField(default=0,blank=True)
    total_scans = models.PositiveBigIntegerField(default=0,blank=True)
    pack_type = models.PositiveBigIntegerField(default=0,blank=True)    # 0 -> Free pack
                                                                        # 1 -> monthly pack
                                                                        # 2 -> yearly pack
    def __str__(self) -> str:
        return f'{self.restaurant.name} pack {self.pack_type}'

class MenuCategory(models.Model):
    restaurant = models.ForeignKey(RestaurantDetail,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=30,null=True)
    order = models.IntegerField(null=True)
    class Meta:
        ordering = ['order']
    def __str__(self) -> str:
        return f'{self.name}'

class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=30,null=True)
    price = models.FloatField(null=True)
    desc = models.TextField(null=True)
    food_type = models.BooleanField(default=True,null=True) #True -> non-veg; False-> Veg;
    img = models.ImageField(upload_to='item_imgs',default='item_imgs/default.png')
    display = models.BooleanField(default=True,null=True)
    start_time = models.TimeField(auto_now=False,null=True,blank=True)
    end_time = models.TimeField(auto_now=False,null=True,blank=True)
    def __str__(self) -> str:
        return f'{self.name}'
def count_total_menu(sender,instance,created,*args,**kwargs):
    restaurant = instance.category.restaurant
    if created:
        pack = Pack.objects.get(restaurant=restaurant)
        pack.total_scans = ScanCount.objects.filter(restaurant=restaurant).count()
        pack.total_menus = MenuItem.objects.filter(category__restaurant=restaurant).count()
        pack.save()
post_save.connect(count_total_menu,sender=MenuItem)

# For Customer's Orders
class OrderedMenu(models.Model):
    menu = models.ForeignKey(MenuItem,on_delete=models.PROTECT,null=True)
    quantity = models.IntegerField(null=True)
    def __str__(self) -> str:
        return f'Order {self.menu.name} Qt{self.quantity}'
    
class CustomerOrder(models.Model):
    order_types = (
        ('dinein','Dinein'),
        ('delivery','Delivery'),
        ('pickup','Pickup')
    )
    restaurant = models.ForeignKey(RestaurantDetail,on_delete=models.CASCADE,null=True)
    customer_name = models.CharField(max_length=30,null=True)
    table_no = models.IntegerField(null=True)
    total_price = models.FloatField(null=True,blank=True)
    success = models.BooleanField(default=False,blank=True,null=True)
    status = models.CharField(max_length=15,default='pending',null=True)
    ordered_menu = models.ManyToManyField(OrderedMenu)
    timestamp = models.DateTimeField(default=datetime.datetime.now())
    order_type = models.CharField(max_length=15,default='dinein',choices=order_types)
    def __str__(self) -> str:
        return f'{self.customer_name} total {self.total_price}'
    class Meta:
        ordering = ['status','-timestamp',]
    @property
    def delete_after_five_minutes(self):
        time = self.timestamp + datetime.timedelta(minutes=1)
        if time < datetime.datetime.now():
            order = CustomerOrder.objects.get(pk=self.pk)
            order.delete()
            return True
        else:
            return False

class BillingDetail(models.Model):
    countries = (
        ('india','India'),
        ('usa','United State of America'),
        ('uae','United Arab Emirates'),
        ('uk','United Kingdom'),

    )
    restaurant = models.OneToOneField(RestaurantDetail,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=30,null=True)
    address = models.CharField(max_length=100,null=True)
    gstin = models.CharField(max_length=15,blank=True,null=True)
    city = models.CharField(max_length=30,null=True)
    state = models.CharField(max_length=30,null=True)
    zipcode = models.CharField(max_length=30,null=True)
    country = models.CharField(max_length=30,choices=countries,default=countries[0][0],null=True)

class AccountSetting(models.Model):
    currenries = (
        ('INR','INR'),
        ('USD','USD'),
        ('SAR','SAR'),
    )
    layouts = (
        ('list','List Layout'),
        ('grid','Grid Layout'),
        ('box','Box Layout'),
    )
    languages = (
        ('english','English'),
        ('tamil','Tamil'),
        ('sakovia','Sakovia'),
    )
    restaurant = models.OneToOneField(RestaurantDetail,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15,blank=True)
    currency_model = models.ForeignKey(Currency,on_delete=models.CASCADE,null=True,blank=True)
    menu_layout = models.CharField(max_length=15,default=layouts[0][0],choices=layouts,null=True,blank=True)
    menu_language = models.CharField(max_length=15,default=languages[0][0],choices=languages,null=True,blank=True)

class ScanCount(models.Model):
    restaurant = models.ForeignKey(RestaurantDetail,on_delete=models.CASCADE,null=True)
    ip = models.CharField(max_length=20,unique=True)
def count_total_scan(sender,instance,created,*args,**kwargs):
    restaurant = instance.restaurant
    if created:
        pack = Pack.objects.get(restaurant=restaurant)
        pack.total_scans = sender.objects.filter(restaurant=restaurant).count()
        pack.save()
post_save.connect(count_total_scan,sender=ScanCount)

class Enquiry(models.Model):
    STATUS_CHOICE = (
        ('initiated','Initiated'),
        ('pending','Pending'),
        ('resolved','Resolved'),
    )
    restaurant = models.ForeignKey(RestaurantDetail,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=50,null=True)
    question = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,default=STATUS_CHOICE[0][0],choices=STATUS_CHOICE)
    def __str__(self):
        return f'{self.restaurant.name}\'s enquiry'
    class Meta:
        ordering = ['-date',]