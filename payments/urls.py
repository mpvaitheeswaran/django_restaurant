from django.urls import path
from payments import views

urlpatterns = [
    path('pay/', views.payment,name='payments-pay'),
    path('response/', views.response,name='payments-response'),
]