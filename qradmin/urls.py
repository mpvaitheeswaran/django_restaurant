from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
   path('',views.admin_dashboard,name='qradmin-dashboard'),
   path('accounts/',views.accounts,name='qradmin-accounts'),
   path('enquiry/',views.enquiry,name='qradmin-enquiry'),
   path('change_pack/',views.changePack,name='qradmin-change_pack'),
]