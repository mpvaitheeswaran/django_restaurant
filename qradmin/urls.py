from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
   path('accounts/',views.accounts,name='qradmin-accounts'),
   path('enquiry/',views.enquiry,name='qradmin-enquiry'),
]