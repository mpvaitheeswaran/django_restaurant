from datetime import datetime
from django import template
from django.utils import timezone

from qrmenu.models import AccountSetting,MenuCategory,MenuItem,ScanCount
register = template.Library()

@register.filter()
def mul(value,arg):
    return value*arg

@register.filter()
def available_time(st,et):
    if st and et:
        if st<=datetime.time(timezone.localtime(timezone.now())) and et>=datetime.time(timezone.localtime(timezone.now())):
            return True
        else:
            return False
    return None

@register.filter()
def phone(value):
    return AccountSetting.objects.get(restaurant=value).phone

@register.filter()
def total_menu(value):
    menu_count = 0
    for category in MenuCategory.objects.filter(restaurant=value):
        for menu in MenuItem.objects.filter(category=category):
            menu_count += 1 
    return menu_count

@register.filter()
def total_scan(value):
    scan_count = ScanCount.objects.filter(restaurant=value).count()
    return scan_count