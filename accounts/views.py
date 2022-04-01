from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .decorators import unauthenticated_user
from qrmenu.models import RestaurantDetail,BillingDetail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.tokens import account_activation_token
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as login_auth
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.conf import settings
from qrmenu.process import html_to_pdf
from io import BytesIO
from django.core.files import File

# Create your views here.
# def testPage(request):
#     return render(request,'accounts/confirm_mail.html')
@unauthenticated_user()
def register(request):
    context = {}
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save() 
            name = request.POST['restaurant_name']
            gstin = request.POST['gstin']
            restaurant = RestaurantDetail.objects.create(user=user,name=name,gstin=gstin)
            billing_detail = BillingDetail.objects.get(restaurant=restaurant)
            billing_detail.gstin = gstin
            billing_detail.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your RestaurantQR account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request,'accounts/confirm_mail.html')
            # return HttpResponse('Please confirm your email address to complete the registration')
            # login_auth(request,user)
            # return redirect('dashboard')
        # context['old_email'] = form.cleaned_data['email']
        context['old_name'] = request.POST['restaurant_name']
        context['old_gstin'] = request.POST['gstin']
        context['form'] = form
        return render(request,'accounts/register.html',context)
    form = RegistrationForm()
    return render(request,'accounts/register.html',{'form':form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login_auth(request,user)
        return redirect('dashboard')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        # return HttpResponse('Activation link is invalid!')
        return render(request,'accounts/invalid_link.html')

@unauthenticated_user(redirect_url='qradmin-dashboard')
def adminLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login_auth(request, user)
                    return redirect('qradmin-dashboard')
                else:
                    messages.error(request,"Unauthenticated User!")
        else:
            return render(request,'accounts/admin_login.html',{'form':form})
    form = AuthenticationForm()
    return render(request,'accounts/admin_login.html',{'form':form})