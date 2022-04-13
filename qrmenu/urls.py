from unicodedata import name
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.dashboard,name='dashboard'),
    path('restaurant/',login_required( views.RestaurantView.as_view()),name='restaurant'),
    path('menu/', login_required(views.MenuView.as_view()),name='menu'),
    path('notifications/', login_required(views.NotificationView.as_view()),name='notifications'),
    path('orders/', login_required(views.OrdersView.as_view()),name='orders'),
    path('approve_order/',views.aproveOrder,name='aprove_order'),
    path('delete_order/',views.deleteOrder,name='delete_order'),
    path('print/<pk>/',login_required(views.BillTemplate.as_view()),name='bill_print'),
    path('delete_old_orders/',views.delete_old_orders,name='delete_old_orders'),
    path('membership/', login_required(views.MembershipView.as_view()),name='membership'),
    path('qr_builder/', views.qrBuilder,name='qr-builder'),
    path('transactions/', login_required(views.TransactionView.as_view()),name='transactions'),
    path('settings/', login_required(views.AccountSettingsView.as_view()),name='accountsettings'),
    path('support/', login_required(views.SupportView.as_view()),name='support'),
    path('changepassword/', views.changePassword,name='changepassword'),
    path('add_category/', views.addCategory,name='add_category'),
    path('edit_category/', views.editCategory,name='edit_category'),
    path('reorder/', views.reorderCategory,name='reorder'),
    path('add_item/', views.addItem,name='add_item'),
    path('update_item/', views.updateItem,name='update_item'),
    path('delete_category/', views.deleteCategory,name='delete_category'),
    path('delete_item/', views.deleteItem,name='delete_item'),
    path('restaurant/<str:unique_id>/<str:name>/', views.CustomerView.as_view(),name='qrmenu-category_list'),
    path('restaurant/<str:unique_id>/<str:name>/menu/<int:category_id>/', views.MenuItemView.as_view(),name='qrmenu-menu_list'),
    path('restaurant/placeorder/', views.placeOrder,name='qrmenu-place_order'),
    path('restaurant/call/', views.callWaiter,name='qrmenu-call_waiter'),
    # Notifications
    path('read_notification/', views.readNotification,name='qrmenu-read_notification'),
    path('invoice/',views.GeneratePdf.as_view(),name='invoice'),
    path('pack/',views.select_pack,name='qrmenu-pack'),
    path('billing_detail/',views.billingDetail,name='qrmenu-enter_detail'),
    path('activate_trial/',views.activateTrial,name='qrmenu-activate_trial')
]