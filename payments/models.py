from django.db import models
from qrmenu.models import RestaurantDetail

# Create your models here.
class PackOrder(models.Model):
    order_id = models.CharField(max_length=10,primary_key=True)
    restaurant = models.ForeignKey(RestaurantDetail,on_delete=models.CASCADE)
    pack_type = models.CharField(max_length=5)
    order_amount = models.CharField(max_length=25)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)
