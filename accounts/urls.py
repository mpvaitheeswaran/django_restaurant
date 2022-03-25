from unicodedata import name
from django.shortcuts import redirect
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.register,name='accounts-register'),
    # Activate an account
    # path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate, name='activate'),
    path('activate/<uidb64>/<token>/',
        views.activate, name='activate'),
    path('login/',auth_views.LoginView.as_view(template_name = 'accounts/login.html',redirect_authenticated_user=True),name='accounts-login'),
    path('login/admin/',views.adminLogin,name='accounts-adminlogin'),
    path('logout/',auth_views.LogoutView.as_view(next_page='accounts-login'),name='accounts-logout'),
    path('password_reset_view/',auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_view.html'),name='password_reset_view'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),
    # path('test/',views.testPage)
]