from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

@user_passes_test(lambda u: u.is_superuser,redirect_field_name=None)
def accounts(request):
    return render(request,'qradmin/accounts.html')

@user_passes_test(lambda u: u.is_superuser,redirect_field_name=None)
def enquiry(request):
    return render(request,'qradmin/enquiry.html')