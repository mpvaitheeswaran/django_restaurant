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
    currency = models.CharField(max_length=5,default='inr',blank=True,null=True)
    invoice_pdf = models.FileField(upload_to='invoice_pdfs',null=True,blank=True)
    class Meta:
        ordering = ['-order_date',]